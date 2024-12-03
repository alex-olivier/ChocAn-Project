import os
# import models
from models import (models, Base, Member, Provider, Service, ProviderService, ServiceRecord)
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
import re

# Database setup
engine = create_engine('sqlite:///chocan.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ChocAn Database Operations

# # Validate user input with retry on failure
# def prompt_until_valid(regex, prompt_message, error_message):
#     while True:
#         value = input(prompt_message)
#         if re.match(regex, value):
#             return value
#         print(error_message)

def add_member(name, street_address, city, state, zip_code):
    try:
        new_member = Member(name=name, street_address=street_address, city=city, state=state, zip_code=zip_code)
        session.add(new_member)  # Triggers validation
        session.commit()
        print(f"Added member: {name}")
    except ValueError as e:
        print(e)

def add_provider(name, street_address, city, state, zip_code):
    try:
        new_provider = Provider(name=name, street_address=street_address, city=city, state=state, zip_code=zip_code)
        session.add(new_provider)
        session.commit()
        print(f"Added provider: {name}")
    except ValueError as e:
        print(e)

def add_service(name, fee):
    service = Service(name=name, fee=fee)
    session.add(service)
    session.commit()
    print(f"Added service: {name} with code {service.code}")

def record_service(provider_number, member_number, service_code, service_date, comments=None):
    provider = session.query(Provider).filter_by(number=provider_number).first()
    member = session.query(Member).filter_by(number=member_number).first()
    service = session.query(Service).filter_by(code=service_code).first()

    if not provider or not member or not service:
        print("Invalid provider, member, or service code.")
        return

    new_service_record = ServiceRecord(
        provider_id=provider.id,
        member_id=member.id,
        service_code=service_code,
        service_date=datetime.datetime.strptime(service_date, "%m-%d-%Y"),
        comments=comments
    )
    session.add(new_service_record)
    session.commit()
    print(f"Service recorded for {member.name} by {provider.name}")


################################################################################
# ADDITIONAL FUNCTIONALITY
################################################################################

# Generates weekly member report
def generate_member_report(member_number):
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

# Generates weekly provider report
def generate_provider_report(provider_number):
    provider = session.query(Provider).filter_by(number=provider_number).first()
    if not provider:
        print("Invalid provider number.")
        return

    records = session.query(ServiceRecord).filter_by(provider_id=provider.id).order_by(ServiceRecord.timestamp).all()
    if not records:
        print("No services recorded for this provider.")
        return

    report_filename = f"{provider.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_ProviderReport.txt"
    with open(report_filename, 'w') as file:
        file.write(f"Provider Name: {provider.name}\n")
        file.write(f"Provider Number: {provider.number}\n")
        file.write(f"Address: {provider.street_address}, {provider.city}, {provider.state} {provider.zip_code}\n\n")
        file.write("Services Provided:\n")
        total_fee = 0
        for record in records:
            member = session.query(Member).get(record.member_id)
            service = session.query(Service).filter_by(code=record.service_code).first()
            total_fee += service.fee
            file.write(f"Date: {record.service_date.strftime('%m-%d-%Y')}, Member: {member.name}, Service: {service.name}, Fee: ${service.fee:.2f}\n")
        file.write(f"\nTotal Consultations: {len(records)}\n")
        file.write(f"Total Fee: ${total_fee:.2f}\n")
    print(f"Provider report generated: {report_filename}")


# For the EFT data, all that is required is that a file be set up containing
# the provider name, provider number, and the amount to be transferred.
def generate_eft_data():
    providers = session.query(Provider).all()
    eft_filename = f"EFT_Data_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(eft_filename, 'w') as file:
        file.write("Provider EFT Data:\n")
        file.write("Provider Name, Provider Number, Total Fee\n")
        for provider in providers:
            records = session.query(ServiceRecord).filter_by(provider_id=provider.id).all()
            total_fee = sum(session.query(Service).filter_by(code=record.service_code).first().fee for record in records)
            if total_fee > 0:
                file.write(f"{provider.name}, {provider.number}, ${total_fee:.2f}\n")
    print(f"EFT data generated: {eft_filename}")


# Summary Report for Manager
def generate_summary_report():
    providers = session.query(Provider).all()
    total_providers = len(providers)
    total_consultations = 0
    total_fee = 0

    for provider in providers:
        records = session.query(ServiceRecord).filter_by(provider_id=provider.id).all()
        total_consultations += len(records)
        total_fee += sum(session.query(Service).filter_by(code=record.service_code).first().fee for record in records)

    report_filename = f"Manager_Summary_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_filename, 'w') as file:
        file.write(f"Total Providers: {total_providers}\n")
        file.write(f"Total Consultations: {total_consultations}\n")
        file.write(f"Total Fee: ${total_fee:.2f}\n")
    print(f"Manager summary report generated: {report_filename}")



# Example usage
if __name__ == "__main__":
    add_member("John Doe", "123456789", "123 Main St", "Anytown", "CA", "90210")
    add_provider("Dr. Smith", "987654321", "456 Elm St", "Othertown", "NY", "10001")
    add_service("598470", "Dietitian Session", 150.00)
    record_service("987654321", "123456789", "598470", "11-24-2024", "Initial consultation")

    # Example usage of additional functionalities
    generate_member_report("123456789")
    generate_provider_report("987654321")
    # generate_eft_data()
    generate_summary_report()
