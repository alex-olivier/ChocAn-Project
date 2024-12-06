from database_manager import DatabaseManager, get_session
from models import Member, Provider, Service, ServiceRecord
from datetime import datetime



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
            
            records = session.query(ServiceRecord).filter_by(member_id=member.id).order_by(ServiceRecord.service_date).all()
            if not records:
                print("No services recorded for this member.")
                return

            report_filename = f"{member.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_MemberReport.txt"
            with open(report_filename, 'w') as file:
                file.write(f"Member Name: {member.name}\n")
                file.write(f"Member Number: {member.number}\n")
                file.write(f"Address: {member.street_address}, {member.city}, {member.state} {member.zip_code}\n\n")
                file.write("Services:\n")
                for record in records:
                    provider = session.query(Provider).get(record.provider_id)
                    service = session.query(Service).filter_by(code=record.service_code).first()
                    file.write(f"Date: {record.service_date.strftime('%m-%d-%Y')}, Provider: {provider.name}, Service: {service.name}\n")
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

            records = session.query(ServiceRecord).filter_by(provider_id=provider.id).order_by(ServiceRecord.timestamp).all()
            if not records:
                print("No services recorded for this provider.")
                return

            report_filename = f"{provider.name.replace(' ', '_')}_ \
                              {datetime.now().strftime('%Y%m%d')}_ \
                              ProviderReport.txt"
            with open(report_filename, 'w') as file:
                file.write(f"Provider Name: {provider.name}\n")
                file.write(f"Provider Number: {provider.number}\n")
                file.write(
                    f"Address: {provider.street_address}, "
                    f"{provider.city}, "
                    f"{provider.state} "
                    f"{provider.zip_code}\n\n"
                )
                file.write("Services Provided:\n")
                total_fee = 0
                for record in records:
                    member = session.query(Member).get(record.member_id)
                    service = session.query(Service).filter_by(code=record.service_code).first()
                    total_fee += service.fee
                    file.write(
                        f"Date: {record.service_date.strftime('%m-%d-%Y')}\n" 
                        f"Member: {member.name}\n" 
                        f"Service: {service.name}\n" 
                        f"Fee: ${service.fee:.2f}\n\n"
                    )
                file.write(f"\nTotal Consultations: {len(records)}\n")
                file.write(f"Total Fee: ${total_fee:.2f}\n")
            print(f"Provider report generated: {report_filename}")


    # # Summary Report for Manager
    # def generate_summary_report(self):
    #     """
    #     A summary report is given to the manager for accounts payable.
    #     The report lists every provider to be paid that week, the number
    #     of consultations each had, and his or her total fee for that week.
    #     Finally the total number of providers who provided services, the
    #     total number of consultations, and the overall fee total are printed.
    #     """
    #     with self.db_manager.get_session() as session:
    #         providers = session.query(Provider).all()
    #         total_providers = len(providers)
    #         total_consultations = 0
    #         total_fee = 0

    #         for provider in providers:
    #             records = session.query(
    #                 ServiceRecord
    #             ).filter_by(
    #                 provider_id=provider.id
    #             ).all()
    #             total_consultations += len(records)
    #             total_fee += sum(
    #                 session.query(
    #                     Service
    #                 ).filter_by(
    #                     code=record.service_code
    #                 ).first().fee for record in records
    #             )

    #         report_filename = f"Manager_Summary_{datetime.now().strftime('%Y%m%d')}.txt"
    #         with open(report_filename, 'w') as file:
    #             file.write("Accounts Payable Summary Report:\n")
    #             file.write(f"Total Providers: {total_providers}\n")
    #             file.write(f"Total Consultations: {total_consultations}\n")
    #             file.write(f"Total Fee: ${total_fee:.2f}\n")
    #         print(f"Manager summary report generated: {report_filename}")
