import base64
import os
import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
import csv

from .models import Record
from .forms import RecordForm


@login_required
def create_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        signature_data = request.POST.get('signature')
      
        if form.is_valid() and signature_data:
            print("form is valid")
            
            # Generate a unique filename using UUID
            unique_filename = f"signature_{uuid.uuid4().hex}.png"
            
            # Extract base64 signature (strip the header if present)
            if signature_data.startswith('data:image/png;base64,'):
                signature_data = signature_data.split('data:image/png;base64,')[1]
            
            # Convert base64 to image
            signature_image = ContentFile(base64.b64decode(signature_data), name=unique_filename)
            
            # Save the image to the 'signature' directory (Django will handle saving it in MEDIA_ROOT)
            form.instance.signature.save(unique_filename, signature_image)
            print("saved the image to the file")
            
            # Save the form with the signature image URL
            form.save()

            return redirect('record_list')  # Redirect to the record list page
        else:
            print(form.errors)
    else:
        form = RecordForm()

    return render(request, 'record/create_record.html', {'form': form})

@login_required
def update_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        signature_data = request.POST.get('signature')

        if form.is_valid():
            # If a new signature is provided, update it
            if signature_data:
                unique_filename = f"signature_{uuid.uuid4().hex}.png"
                if signature_data.startswith('data:image/png;base64,'):
                    signature_data = signature_data.split('data:image/png;base64,')[1]
                signature_image = ContentFile(base64.b64decode(signature_data), name=unique_filename)
                record.signature.save(unique_filename, signature_image)

            form.save()
            return redirect('record_list')  # Redirect after saving the form
        else:
            print(form.errors)
    else:
        form = RecordForm(instance=record)

    return render(request, 'record/update_record.html', {'form': form, 'record': record})

@login_required
def record_list(request):
    records = Record.objects.all()
    return render(request, 'record/record_list.html', {'records': records})

@login_required
def complete_record(request, record_id): 
    record = get_object_or_404(Record, pk=record_id)
    if record:
        record.time_out = timezone.now()  # Set the current time as time_out
        record.save()
        messages.success(request, 'Attendance marked as completed successfully.')
        return redirect('record_list') 
    else:
        messages.error(request, 'Record not found.')
        return redirect('record_list')

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    if record:
        record.delete()
        messages.success(request, 'Record deleted successfully.')
        return redirect('record_list') 
    else:
        messages.error(request, 'Record not found.')
        return redirect('record_list')

@login_required
def generate_report(request):
    # Get the start and end date from the request parameters
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date and end_date:
        # Convert string to datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        records = Record.objects.filter(time_in__range=[start_date, end_date])
       
    else:
        records = Record.objects.all()
    if not records:
        messages.error(request, "No records found for the given date range.")
        return redirect('record_list')

    filename = f'{start_date.strftime("%Y_%m_%d")}_to_{end_date.strftime("%Y_%m_%d")}_attendance_report.csv'

    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create the CSV writer and write the header
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Station', 'Time In', 'Time Out'])

    # Write records to CSV
    for record in records:
        writer.writerow([record.fname, record.lname, record.station.name, record.time_in, record.time_out])

    return response