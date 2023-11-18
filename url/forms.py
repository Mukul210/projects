from django import forms


class Url(forms.Form):
    url = forms.CharField(label="URL")


from .models import Shortener, Category




class ShortenerForm(forms.ModelForm):

    class Meta:
        model = Shortener
        exclude = ['user', 'times_followed', 'short_url']
        #fields = ('long_url',)




class TopicForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ["user"]
        #fields = '__all__'