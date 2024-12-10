import os
from datetime import datetime
from datetime import timedelta
from chocan_software.models import Member
from chocan_software.models import Provider
from chocan_software.models import Service
from chocan_software.models import ServiceRecord
from chocan_software.data_managers.database_manager import DatabaseManager


class ReportManager:
    """
    ReportManager contains methods for managing the generation of reports, EFT
    Data, and the Provider Directory.
    """
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager is not None else DatabaseManager()
        self.reports_dir = os.path.join(os.path.dirname(__file__), "../../reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_member_report(self, member_number):
        """
        Generates weekly member report containing all the services they have
        received in the past week.
        """
        member_id = int(member_number)
        one_week_ago = datetime.now() - timedelta(days=7)
        
        with self.db_manager.get_session() as session:
            member = session.query(Member).filter_by(id=member_id).first()
            if not member:
                print("\nInvalid member number.")
                return   
            records = session.query(ServiceRecord).filter(
                ServiceRecord.member_id == member.id,
                ServiceRecord.service_date >= one_week_ago
            ).order_by(ServiceRecord.service_date).all()
            if not records:
                return

            report_filename = os.path.join(
                self.reports_dir,
                f"{member.name.replace(' ', '_')}_"
                f"{datetime.now().strftime('%Y%m%d')}_"
                "MemberReport.txt"
            )
            with open(report_filename, 'w') as file:
                file.write(
                    "╔═════════════════════════════════════════════════════╗\n"
                    "║                Chocoholics Anonymous                ║\n"
                    "╚═════════════════════════════════════════════════════╝\n"
                    "Member Weekly Report\n\n"
                    "Member Information:\n"
                    f"  Name:     {member.name}\n"
                    f"  Number:   {member.id:09}\n"
                    f"  Street:   {member.street_address}\n"
                    f"  City:     {member.city}\n"
                    f"  State:    {member.state}\n"
                    f"  ZIP Code: {member.zip_code}\n\n"
                )
                file.write("Services:\n")
                for record in records:
                    provider = session.query(Provider).get(record.provider_id)
                    service = session.query(Service).filter_by(
                        id=record.service_id
                    ).first()
                    file.write(
                        f"Date of service: {record.service_date.strftime('%m-%d-%Y')}\n"
                        f"Provider name: {provider.name}\n"
                        f"Service name: {service.name}\n\n"
                    )
            print(f"Member report generated: {report_filename}")

    def generate_provider_report(self, provider_number):
        """
        Generates weekly report for Providers containing all the services they
        have provided to members in the past week.
        """
        provider_id = int(provider_number)
        one_week_ago = datetime.now() - timedelta(days=7)
        with self.db_manager.get_session() as session:
            provider = session.query(Provider).filter_by(id=provider_id).first()
            if not provider:
                print("\nInvalid provider number.")
                return
            records = session.query(ServiceRecord).filter(
                ServiceRecord.provider_id == provider.id,
                ServiceRecord.service_date >= one_week_ago
            ).order_by(ServiceRecord.service_date).all()
            if not records:
                return

            report_filename = os.path.join(
                self.reports_dir,
                f"{provider.name.replace(' ', '_')}_"
                f"{datetime.now().strftime('%Y%m%d')}_"
                "ProviderReport.txt"
            )
            with open(report_filename, 'w') as file:
                file.write(
                    "╔═════════════════════════════════════════════════════╗\n"
                    "║                Chocoholics Anonymous                ║\n"
                    "╚═════════════════════════════════════════════════════╝\n"
                    "Provider Weekly Report\n\n"
                    "Provider Information:\n"
                    f"  Name:     {provider.name}\n"
                    f"  Number:   {provider.id:09}\n"
                    f"  Street:   {provider.street_address}\n"
                    f"  City:     {provider.city}\n"
                    f"  State:    {provider.state}\n"
                    f"  ZIP Code: {provider.zip_code}\n\n"
                )
                file.write(f"Services provided from "
                           f"{one_week_ago.strftime('%m-%d-%Y')} to "
                           f"{datetime.now().strftime('%m-%d-%Y')}:\n"
                )
                total_weekly_fee = 0
                for record in records:
                    member = session.query(Member).get(record.member_id)
                    service = session.query(Service).filter_by(
                        id=record.service_id
                    ).first()
                    total_weekly_fee += service.fee
                    file.write(
                        f"  Date of Service: {record.service_date.strftime('%m-%d-%Y')}\n" 
                        f"  Database Timestamp: {record.timestamp.strftime('%m-%d-%Y %H:%M:%S')}\n"
                        f"  Member Name: {member.name}\n"
                        f"  Member Number: {member.id:09}\n"
                        f"  Service Code: {service.id:06}\n" 
                        f"  Service Fee: $ {service.fee:.2f}\n\n"
                    )
                file.write(f"Total Consultations: {len(records)}\n")
                file.write(f"Total Fee: $ {total_weekly_fee:.2f}\n")
            print(f"Provider report generated: {report_filename}")

    def generate_summary_report(self):
        """
        A summary report is given to the manager for accounts payable.
        The report lists every provider to be paid that week.
        """
        one_week_ago = datetime.now() - timedelta(days=7)
        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()
            provider_total = 0
            consultation_total = 0
            fee_grand_total = 0
        
            report_filename = os.path.join(
                self.reports_dir,
                "Manager_Summary_"
                f"{datetime.now().strftime('%Y%m%d')}.txt"
            )
            with open(report_filename, 'w') as file:
                file.write(
                    "╔═════════════════════════════════════════════════════╗\n"
                    "║                Chocoholics Anonymous                ║\n"
                    "╚═════════════════════════════════════════════════════╝\n"
                    "Accounts Payable Weekly Summary Report\n"
                    f"Week of {one_week_ago.strftime('%m-%d-%Y')}\n\n"
                    "────────────┬───────────────────────────┬───────┬────────────\n"
                    " PROVIDER # │ PROVIDER NAME             │ CONS¹ │ FEE TOTAL\n"
                    "────────────┼───────────────────────────┼───────┼────────────\n"
                )
                for provider in providers:
                    records = session.query(ServiceRecord).filter(
                        ServiceRecord.provider_id == provider.id,
                        ServiceRecord.service_date >= one_week_ago
                    ).order_by(ServiceRecord.service_date).all()
                    record_count = len(records)
                    if record_count == 0:
                        continue
                    provider_fee_total = sum(
                        session.query(Service).filter_by(
                            id=record.service_id
                        ).first().fee for record in records
                    )
                    file.write(
                        f" {provider.id:09}  "
                        f"│ {provider.name:<25} "
                        f"│  {record_count:>3}  "
                        f"│ ${provider_fee_total:>8.2f}\n"
                    )
                    provider_total += 1
                    consultation_total += len(records)
                    fee_grand_total += provider_fee_total
                file.write(
                    "────────────┴───────────────────────────┴───────┴────────────\n"
                    " ¹: Consultationss\n\n"
                    f"Total Providers...................... {provider_total}\n"
                    f"Total Consultations.................. {consultation_total}\n"
                    f"Total Fees........................... $ {fee_grand_total:.2f}\n"
                )
        print(f"Summary report generated: {report_filename}")

    def generate_eft_data(self):
        """
        Generates a file containing EFT data meant for the payment processor.
        The file contains the provider name, provider number, and the amount to
        be transferred.
        """
        one_week_ago = datetime.now() - timedelta(days=7)

        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()
            
            eft_filename = os.path.join(
                self.reports_dir,
                f"EFT_Data_{datetime.now().strftime('%Y%m%d')}.txt"
            )
            with open(eft_filename, 'w') as file:
                file.write("provider_name,provider_number,amount\n")
                for provider in providers:
                    records = session.query(ServiceRecord).filter(
                        ServiceRecord.provider_id == provider.id,
                        ServiceRecord.service_date >= one_week_ago
                    ).order_by(ServiceRecord.service_date).all()
                    total_fee = sum(
                        session.query(Service).filter_by(
                            id=record.service_id
                        ).first().fee for record in records
                    )
                    file.write(f"{provider.name},"
                               f"{provider.id:09},"
                               f"{total_fee:.2f}\n"
                    )
        print(f"EFT data generated: {eft_filename}")

    def main_accounting_procedure(self):
        """
        Main accounting procedure runs reports for all providers and members with
        service records from the past week, generates the EFT data, and generates
        the summary report.
        """
        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()
            for provider in providers:
                self.generate_provider_report(provider.id)
            members = session.query(Member).all()
            for member in members:
                self.generate_member_report(member.id)
        self.generate_eft_data()
        self.generate_summary_report()
        print("Main accounting procedure complete.")
  
    def generate_provider_directory(self):
        """
        Generates Provider Directory which contains a list of all the services,
        their codes, and their fees.
        """
        with self.db_manager.get_session() as session:
            services = session.query(Service).all()
            
            directory_filename = os.path.join(
                self.reports_dir,
                "ProviderDirectory_"
                 f"{datetime.now().strftime('%Y%m%d')}.txt"
            )
            with open(directory_filename, 'w') as file:
                file.write("       Provider Directory of Services\n")
                file.write("┌────────┬──────────────────────┬──────────┐\n")
                file.write("│ CODE   │ NAME                 │ FEE      │\n")
                file.write("├────────┼──────────────────────┼──────────┤\n")
                for service in services:
                    file.write(
                        f"│ {service.id:06} "
                        f"│ {service.name:<20} "
                        f"│ $ {service.fee:>6.2f} │\n" 
                    )
                file.write("└────────┴──────────────────────┴──────────┘\n")
        print(f"Provider directory generated: {directory_filename}")
