from django import forms
from dal import autocomplete
from django.core.mail import send_mail

from .models import Member, MedicalRecord, Car, EmergencyContact, ShortNotice

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('profile_image', 'user', 'name', 'middlename', 'first_surname', 'second_surname', 'rut', 'birth_date', 'enrollment_date', 'phone_number', 'use_middlename', 'use_second_surname' )
        widgets = {
            'user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'first_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'second_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'use_middlename': forms.CheckboxInput(attrs={'class': 'form-check-inline'}),
            'use_second_surname': forms.CheckboxInput(attrs={'class': 'form-check-inline'}),
            'profile_image': forms.FileInput(
                attrs={
                    'class': 'form-control form-control'
                }),
        }
        labels = {
            'name': 'Nombre',
            'middlename': 'Segundo Nombre',
            'first_surname': 'Apellido Paterno',
            'second_surname': 'Apellido Materno',
            'rut': 'RUT',
            'birth_date': 'Fecha de Nacimiento',
            'enrollment_date': 'Fecha de Ingreso',
            'phone_number': 'Número de Teléfono',
            'use_middlename': 'Usar Segundo Nombre',
            'use_second_surname': 'Usar Apellido Materno',
            'profile_image': 'Foto de Perfil (max 2MB)',
        }
        exclude = ['user']
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class MedicalForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('no_medical_record', 'sicknesses', 'medications', 'risks')
        widgets = {
            'member': forms.HiddenInput(),
            'no_medical_record': forms.CheckboxInput(attrs={'class': 'form-check-inline'}),
            'sicknesses': forms.TextInput(attrs={'class': 'form-control'}),
            'medications': forms.TextInput(attrs={'class': 'form-control'}),
            'risks': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'no_medical_record': 'No tengo nada que ingresar.',
            'sicknesses': 'Enfermedades',
            'medications': 'Medicamentos',
            'risks': 'Riesgos',
        }
        exclude = ['member']
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('alias', 'brand', 'model', 'year', 'license_plate', 'color')
        widgets = {
            'member': forms.HiddenInput(),
            'alias': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'alias': 'Alias (para identificarlo: Mi Auto, Auto de mi Hermana, etc.)',
            'brand': 'Marca',
            'model': 'Modelo',
            'year': 'Año',
            'license_plate': 'Patente',
            'color': 'Color',
        }
        exclude = ['member']
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ('name', 'phone_number', 'email', 'main_contact', 'relationship')
        widgets = {
            'member': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'main_contact': forms.CheckboxInput(attrs={'class': 'form-check-inline'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre Completo',
            'phone_number': 'Número de Teléfono',
            'email': 'Correo Electrónico',
            'main_contact': '¿Es tu contacto predeterminado?',
            'relationship': 'Relación / Grado de Parentesco (Papá, Mamá, Tío, Tía, etc.)',
        }
        exclude = ['member']
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class ShortNoticeForm(forms.ModelForm):
    class Meta:
        model = ShortNotice
        fields = ('category', 'location', 'route', 'start_date', 'max_end_date', 'participants', 'cau_contact', 'cars', 'description')
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control form-select'}),
            'start_date': forms.DateTimeInput(
                format= '%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control',
                    }
                ),
            'max_end_date': forms.DateTimeInput(
                format= '%Y-%m-%dT%H:%M',  
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'help_text': "<span class='tooltip'>?<span class='tooltiptext'>Recuerda que debes tener señal para notificar tu llegada antes de esta hora. Si no hay notificación al superar el plazo, se activarán las alertas del club.</span></span>",
                    }
                ),
            'cau_contact': autocomplete.ModelSelect2(
                url='avisos:member_autocomplete',
                attrs={
                    'data-placeholder': 'Buscar'
                    }
                ),
            'participants': autocomplete.ModelSelect2Multiple(
                url='avisos:member_autocomplete',
                attrs={
                    'data-placeholder': 'Buscar'
                    }
                ),
            'cars': autocomplete.ModelSelect2Multiple(
                url='avisos:cars_autocomplete',
                forward=['participants'],
                attrs={
                    'data-placeholder': 'Buscar'
                    }
                ),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'location': 'Lugar',
            'category': 'Categoría*',
            'route': 'Ruta(s)',
            'start_date': 'Fecha de Inicio*',
            'max_end_date': 'Plazo Máximo de Llegada*: Recuerda que debes tener señal para notificar tu llegada antes de esta hora. Si no hay notificación al superar el plazo, se activarán las alertas del club.',
            'participants': 'Miembros de la cordada',
            'cau_contact': 'Contacto CAU',
            'cars': 'Vehículos',
            'description': 'Comentarios',
        }
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class SendNoticeForm(forms.ModelForm):
    sendto_caucontacts_fake = forms.BooleanField(required=False, label='Enviar a contactos CAU', widget=forms.CheckboxInput(attrs={'class': 'form-check-inline big-checkbox', 'disabled': True, 'checked': True}))
    sendto_participants_fake = forms.BooleanField(required=False, label='Enviar a cordada', widget=forms.CheckboxInput(attrs={'class': 'form-check-inline big-checkbox', 'disabled': True, 'checked': True}))
    sendto_board_fake = forms.BooleanField(required=False, label='Enviar a directiva', widget=forms.CheckboxInput(attrs={'class': 'form-check-inline big-checkbox', 'disabled': True, 'checked': True}))
    sendto_emergencycontacts = forms.BooleanField(required=False, label='Enviar a contactos de emergencia', widget=forms.CheckboxInput(attrs={'class': 'form-check-inline big-checkbox', 'checked': True}))
    sendto_caumembers = forms.BooleanField(required=False, label='Enviar a Google Group CAU', widget=forms.CheckboxInput(attrs={'class': 'form-check-inline big-checkbox', 'checked': True}))
    sendto_otheremails = forms.CharField(required=False, label='Incluir otros correos electrónicos (sepáralos con comas ",")', widget=forms.TextInput(attrs={'class': 'form-control email-addresses'}))
    mail_body = forms.CharField(required=False, label='Mensaje', widget=forms.Textarea(attrs={'class': 'form-control'}))

    sendto_caucontacts = forms.BooleanField(required=False, initial=True, label='Enviar a contactos CAU', widget=forms.HiddenInput())
    sendto_participants = forms.BooleanField(required=False, initial=True, label='Enviar a cordada', widget=forms.HiddenInput())
    sendto_board = forms.BooleanField(required=False, initial=True, label='Enviar a directiva', widget=forms.HiddenInput())

    class Meta:
        model = ShortNotice
        fields = ()
        widgets = {
            'sent_date': forms.HiddenInput(),
            'sent_by': forms.HiddenInput(),
        }
        exclude = ['sent_date', 'sent_by']
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())

    def save(self, commit=True):
        instance = super(SendNoticeForm, self).save(commit = False)
        instance.email_recipients.clear()
        if self.cleaned_data['sendto_caucontacts']:
            instance.include_caucontacts()
        if self.cleaned_data['sendto_participants']:
            instance.include_participants()
        if self.cleaned_data['sendto_board']:
            instance.include_board()
        if self.cleaned_data['sendto_emergencycontacts']:
            instance.include_emergencycontacts()
        if self.cleaned_data['sendto_caumembers']:
            instance.include_caumembers()
        
        list_of_mails = self.cleaned_data['sendto_otheremails'].strip('[]').split(',')
        for email in list_of_mails:
            email = email.replace('"', '')
            instance.include_email(email)

        mail_content = self.cleaned_data['mail_body']

        if commit:
            instance.save()
            instance.publish_notice(mail_content = mail_content)

        return instance

class ArrivedNoticeForm(forms.ModelForm):
    class Meta:
        model = ShortNotice
        fields = ()
        widgets = {
            'arrival_confirmation_date': forms.HiddenInput(),
            'arrival_confirmation_by': forms.HiddenInput(),
        }
        exclude = ['arrival_confirmation_date', 'arrival_confirmation_by']
        action = forms.CharField(max_length=60, widget=forms.HiddenInput())
    
    def save(self, commit=True):
        instance = super(ArrivedNoticeForm, self).save(commit = False)

        if commit:
            instance.save()
            instance.notify_arrival()

        return instance