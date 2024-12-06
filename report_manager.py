from database_manager import DatabaseManager, get_session
from models import Member, Provider, Service, ServiceRecord
from datetime import datetime, timedelta


class ReportManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    # Generates Provider Directory
    def generate_provider_directory(self):
        """
        An alphabetically ordered list of service names
        and corresponding service codes and fees.
        """
        with get_session() as session:
            services = session.query(Service).all()
            directory_filename = f"ProviderDirectory_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(directory_filename, 'w') as file:
                file.write("Provider Directory:\n")
                file.write("Service Code, Service Name, Fee\n")
                for service in services:
                    file.write(f"{service.code}, {service.name}, ${service.fee:.2f}\n")
            print(f"Provider directory generated: {directory_filename}")

    # Generates weekly member report
    def generate_member_report(self, member_number):
        """
        Each member who has consulted a ChocAn provider during
        that week receives a list of services provided to that
        member, sorted in order of service date. The report
        includes:
            • Member name                               -> member.name
            • Member number                             -> member.number
            • Member street address                     -> member.street_address
            • Member city                               -> member.city
            • Member state                              -> member.state
            • Member zip code                           -> member.zip_code

            • List of services provided during that week, sorted in
            order of service date. For each service provided, the
            following details are required:
                o Date of service (MM-DD-YYYY)          -> record.service_date
                o Provider name                         -> provider.name
                o Service name                          -> service.name
        """
        with self.db_manager.get_session() as session:
            member = session.query(Member).filter_by(number=member_number).first()
            if not member:
                print("Invalid member number.")
                return
            
            one_week_ago = datetime.now() - timedelta(weeks=1)
            records = session.query(ServiceRecord).filter(
                ServiceRecord.member_id == member.id,
                ServiceRecord.date_of_service >= one_week_ago
            ).order_by(ServiceRecord.date_of_service).all()
            if not records:
                print("No services recorded for this member.")
                return

            report_filename = f"{member.name.replace(' ', '_')}_ \
                                {datetime.now().strftime('%Y%m%d')}_ \
                                MemberReport.txt"
            with open(report_filename, 'w') as file:
                file.write(
                    f"Member name: {member.name}\n"
                    f"Member number: {member.number}\n"
                    f"Member street address: {member.street_address}\n"
                    f"Member city: {member.city}\n"
                    f"Member state: {member.state}\n"
                    f"Member ZIP code: {member.zip_code}\n\n"
                )

                file.write("Services:\n")
                for record in records:
                    provider = session.query(Provider).get(record.provider_id)
                    service = session.query(Service).filter_by(code=record.service_code).first()
                    file.write(
                        f"Date of service: {record.service_date.strftime('%m-%d-%Y')}\n"
                        f"Provider name: {provider.name}\n"
                        f"Service name: {service.name}\n\n"
                    )
            print(f"Member report generated: {report_filename}")


    # Generates weekly report for Providers
    def generate_provider_report(self, provider_number):
        """
        For providers that have provided a service within the last week,
        generate a report containing the list of services they have provided
        to ChocAn members. At the end of the weekly report is a summary
        including the total number of services provided and the total fee from
        the services provided. The report must include:
            • Provider name                             -> provider.name
            • Provider number                           -> provider.number
            • Provider street address                   -> provider.street_address
            • Provider city                             -> provider.city
            • Provider state                            -> provider.state
            • Provider zip code                         -> provider.zip_code

            • List of services provided during that week. For each service
            provided, the following details are required:
                o Date of service (MM-DD-YYYY)          -> record.service_date
                o DB Timestamp (MM-DD-YYYY HH:MM:SS)    -> record.timestamp
                o Member name                           -> member.name
                o Member number                         -> member.number
                o Service code                          -> service.code
                o Fee to be paid (up to $999.99)        -> service.fee

            • Total # of services provided (3 digits)   -> count of services
            • Weekly fee total (up to $99,999.99)       -> sum of fees list
        """
        with self.db_manager.get_session() as session:
            provider = session.query(Provider).filter_by(number=provider_number).first()
            if not provider:
                print("Invalid provider number.")
                return
            
            one_week_ago = datetime.now() - timedelta(weeks=1)
            records = session.query(ServiceRecord).filter(
                ServiceRecord.provider_id == provider.id,
                ServiceRecord.timestamp >= one_week_ago
            ).order_by(ServiceRecord.date_of_service).all()

            if not records:
                print("No services recorded for this provider in the past week.")
                return

            report_filename = f"{provider.name.replace(' ', '_')}_ \
                                {datetime.now().strftime('%Y%m%d')}_ \
                                ProviderReport.txt"
            with open(report_filename, 'w') as file:
                file.write(
                    f"Provider name: {provider.name}\n"
                    f"Provider number: {provider.number}\n"
                    f"Provider street address: {provider.street_address}\n"
                    f"Provider city: {provider.city}\n"
                    f"Provider state: {provider.state}\n"
                    f"Provider ZIP code: {provider.zip_code}\n\n"
                )
                file.write("Services Provided:\n")
                total_weekly_fee = 0
                for record in records:
                    member = session.query(Member).get(record.member_id)
                    service = session.query(Service).filter_by(code=record.service_code).first()
                    total_weekly_fee += service.fee
                    file.write(
                        f"  Date of service: {record.service_date.strftime('%m-%d-%Y')}\n" 
                        f"  Database timestamp: {record.timestamp.strftime('%m-%d-%Y %H:%M:%S')}\n"
                        f"  Member name: {member.name}\n"
                        f"  Member number: {member.number}\n"
                        f"  Service code: {service.code}\n" 
                        f"  Service fee: $ {service.fee:.2f}\n\n"
                    )
                file.write(f"Total Consultations: {len(records)}\n")
                file.write(f"Total Fee: $ {total_weekly_fee:.2f}\n")
            print(f"Provider report generated: {report_filename}")


    # Accounts Payable Summary Report for Manager
    def generate_summary_report(self):
        """
        A summary report is given to the manager for accounts payable.
        The report lists every provider to be paid that week.
        """
        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()
            total_providers = 0
            total_consultations = 0
            total_fees = 0
            
            one_week_ago = datetime.now() - timedelta(weeks=1)
            report_filename = f"Manager_Summary_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(report_filename, 'w') as file:
                file.write(
                    "╔════════════════════════════════╗\n"
                    "║ Chocoholics Anonymous (ChocAn) ║\n"
                    "╚════════════════════════════════╝\n"
                    "Accounts Payable Weekly Summary Report\n"
                    f"WEEK OF: {one_week_ago.strftime('%m-%d-%Y')}\n\n"
                    "────────────┬────────────────────────────┬───────┬────────────\n"
                    " PROVIDER # │ PROVIDER NAME              │ CONS¹ │ FEE TOTAL\n"
                    "────────────┼────────────────────────────┼───────┼────────────\n"
                )
                for provider in providers:
                    records = session.query(ServiceRecord).filter(
                        ServiceRecord.provider_id == provider.id,
                        ServiceRecord.timestamp >= one_week_ago
                    ).order_by(ServiceRecord.timestamp).all()
                    record_count = len(records)
                    if record_count != 0:
                        for record in records:
                            fee_total += session.query(Service).filter_by(
                                code=record.service_code
                            ).first().fee
                        file.write(f" {provider.number:<9}  │ {provider.name:<25} │  {record_count:>3}  │ $ {fee_total:>8.2f}\n")
                        total_providers += 1
                        total_consultations += len(records)
                        total_fees += fee_total
                file.write(
                    "────────────┴────────────────────────────┴───────┴────────────\n"
                    " ¹: Consultationss\n\n"
                    f"Total Providers...................... {total_providers}\n"
                    f"Total Consultations.................. {total_consultations}\n"
                    f"Total Fees........................... $ {total_fees:.2f}\n"
                )
            print(f"Manager summary report generated: {report_filename}")


"""
file.write("╔════════════════════════════════╗\n")
file.write("║ Chocoholics Anonymous (ChocAn) ║\n")
file.write("╚════════════════════════════════╝\n")
file.write("Accounts Payable Weekly Summary Report\n")
file.write("WEEK OF: 01-01-2021\n\n")
file.write("────────────┬────────────────────────────┬───────┬────────────\n")
file.write(" PROVIDER # │ PROVIDER NAME              │ CONS¹ │ FEE TOTAL\n")
file.write("────────────┼────────────────────────────┼───────┼────────────\n")
file.write(f" {provider_number:<9}  │ {provider_name:<25}  │  {consultations:>3}  │ $ {weekly_fee:>8.2f} \n")
file.write("────────────┴────────────────────────────┴───────┴────────────\n")
file.write(" ¹: Consultationss\n\n")
file.write(f"Weekly Total Providers...................... {total_providers}\n")
file.write(f"Weekly Total Consultations.................. {total_consultations}\n")
file.write(f"Weekly Total Fee............................ $ {total_fee:.2f}\n")


 PROVIDER # │ PROVIDER NAME              │ CONS¹ │ FEE TOTAL  
 ───────────┼────────────────────────────┼───────┼───────────
 123456789  │ John Smith                 │   20  │ $  1500.00
 987654321  │ Mary Johnson               │   30  │ $  2800.00
 456789123  │ Robert Brown               │   12  │ $   850.00
 999999999  │ MaximumPossibleNameLength  │  999  │ $ 99999.99
 000000000  │ Short Name                 │    1  │ $     0.01

Weekly Total Providers.................... 99
Weekly Total Consultations................ 9999
Weekly Total Fee.......................... $ 9,999,999.99

"""