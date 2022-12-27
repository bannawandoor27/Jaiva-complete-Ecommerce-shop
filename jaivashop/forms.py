from django.forms import ModelForm
from jaivashop.models import ContactMessage

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['user_name', 'email', 'message',]