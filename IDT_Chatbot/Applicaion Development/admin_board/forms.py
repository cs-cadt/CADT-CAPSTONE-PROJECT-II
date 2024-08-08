from django import forms
from secretkey.models import SecretKey

class LoginForm(forms.Form):
    
    username = forms.CharField(
        widget = forms.TextInput(attrs={
            'class':'form-control' , 'placeholder':'Username'
        }),
        
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control','placeholder':'Password' 
        }),
        )

class SecretKeyForm(forms.ModelForm):
    class Meta:
        model = SecretKey
        fields = ['name', 'secret_key', 'status']

class SecretKeyUpdateForm(forms.ModelForm):
    class Meta:
        model = SecretKey
        fields = ['name']

class DatasetUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')

class TrainModelForm(forms.Form):
    file_name = forms.ChoiceField(choices=[], label='Select Dataset')
    model_name = forms.CharField(max_length=100, label='Model Name')

    def __init__(self, *args, **kwargs):
        dataset_choices = kwargs.pop('dataset_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['file_name'].choices = dataset_choices


