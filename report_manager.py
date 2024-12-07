import os
from database_manager import DatabaseManager
from models import Member, Provider, Service, ServiceRecord
from datetime import datetime, timedelta


class ReportManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    # Generates weekly member report
    def generate_member_report(self, member_number):
        member_id = int(member_number)
        one_week_ago = datetime.now() - timedelta(weeks=1)
        
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
                # print("\nNo services recorded for this member.")
                return

            report_filename = (
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
                    service = session.query(Service).filter_by(id=record.service_id).first()
                    file.write(
                        f"Date of service: {record.service_date.strftime('%m-%d-%Y')}\n"
                        f"Provider name: {provider.name}\n"
                        f"Service name: {service.name}\n\n"
                    )
            print(f"\nMember report generated: {report_filename}")

    # Generates weekly report for Providers
    def generate_provider_report(self, provider_number):
        provider_id = int(provider_number)
        one_week_ago = datetime.now() - timedelta(weeks=1)
        with self.db_manager.get_session() as session:
            provider = session.query(Provider).filter_by(id=provider_id).first()
            if not provider:
                print("\nInvalid provider number.")
                return
            
            records = session.query(ServiceRecord).filter(
                ServiceRecord.provider_id == provider.id,
                ServiceRecord.timestamp >= one_week_ago
            ).order_by(ServiceRecord.service_date).all()
            if not records:
                # print("No services recorded for this provider in the past week.")
                return

            report_filename = (
                f"{provider.name.replace(' ', '_')}"
                f"_{datetime.now().strftime('%Y%m%d')}"
                "_ProviderReport.txt"
            )
            with open(report_filename, 'w') as file:
                file.write(
                    "╔═════════════════════════════════════════════════════╗\n"
                    "║                Chocoholics Anonymous                ║\n"
                    "╚═════════════════════════════════════════════════════╝\n"
                    "Provider Weekly Report\n\n"
                    # f"WEEK OF: {one_week_ago.strftime('%m-%d-%Y')}\n\n"
                    "Provider Information:\n"
                    f"  Name:     {provider.name}\n"
                    f"  Number:   {provider.id:09}\n"
                    f"  Street:   {provider.street_address}\n"
                    f"  City:     {provider.city}\n"
                    f"  State:    {provider.state}\n"
                    f"  ZIP Code: {provider.zip_code}\n\n"
                )

                file.write(
                    f"Services provided from "
                    f"{one_week_ago.strftime('%m-%d-%Y')} to "
                    f"{datetime.now().strftime('%m-%d-%Y')}:\n"
                )
                total_weekly_fee = 0
                for record in records:
                    member = session.query(Member).get(record.member_id)
                    service = session.query(Service).filter_by(id=record.service_id).first()
                    total_weekly_fee += service.fee
                    file.write(
                        f"  Date of service: {record.service_date.strftime('%m-%d-%Y')}\n" 
                        f"  Database timestamp: {record.timestamp.strftime('%m-%d-%Y %H:%M:%S')}\n"
                        f"  Member name: {member.name}\n"
                        f"  Member number: {member.id:09}\n"
                        f"  Service code: {service.id:03}\n" 
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
        one_week_ago = datetime.now() - timedelta(weeks=1)
        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()
            total_providers = 0
            total_consultations = 0
            total_fees = 0
        
            report_filename = f"Manager_Summary_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(report_filename, 'w') as file:
                file.write(
                    "╔═════════════════════════════════════════════════════╗\n"
                    "║                Chocoholics Anonymous                ║\n"
                    "╚═════════════════════════════════════════════════════╝\n"
                    "Accounts Payable Weekly Summary Report\n"
                    f"WEEK OF: {one_week_ago.strftime('%m-%d-%Y')}\n\n"
                    "────────────┬────────────────────────────┬───────┬────────────\n"
                    " PROVIDER # │ PROVIDER NAME              │ CONS¹ │ FEE TOTAL\n"
                    "────────────┼────────────────────────────┼───────┼────────────\n"
                )
                for provider in providers:
                    fee_total = 0
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
                        file.write(f" {provider.id:09}  │ {provider.name:<25} │  {record_count:>3}  │ $ {fee_total:>8.2f}\n")
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

    # For the EFT data, all that is required is that a file be set up containing
    # the provider name, provider number, and the amount to be transferred.
    def generate_eft_data(self):
        one_week_ago = datetime.now() - timedelta(weeks=1)

        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()

            eft_filename = f"EFT_Data_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(eft_filename, 'w') as file:
                file.write("Provider EFT Data:\n")
                file.write("Provider Name, Provider Number, Total Fee\n")
                for provider in providers:
                    records = session.query(ServiceRecord).filter(
                        ServiceRecord.provider_id == provider.id,
                        ServiceRecord.timestamp >= one_week_ago
                    ).order_by(ServiceRecord.service_date).all()
                    total_fee = sum(session.query(Service).filter_by(id=record.service_id).first().fee for record in records)
                    
                    if total_fee > 0:
                        file.write(f"{provider.name}, {provider.id:09}, ${total_fee:.2f}\n")
            print(f"> EFT data generated: {eft_filename}")

    def main_accounting_procedure(self):
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

    # Generates Provider Directory
    def generate_provider_directory(self):
        with self.db_manager.get_session() as session:
            services = session.query(Service).all()
            directory_filename = f"ProviderDirectory_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(directory_filename, 'w') as file:
                file.write("Provider Directory:\n")
                file.write("Service Code, Service Name, Fee\n")
                for service in services:
                    file.write(f"{service.code}, {service.name}, ${service.fee:.2f}\n")
            print(f"Provider directory generated: {directory_filename}")