from django import forms
from rango.models import Page, Category


class CategoryForm(forms.ModelForm):
    maxLengthName = Category._meta.get_field('name').max_length

    name = forms.CharField(max_length= maxLengthName,
                           help_text="Please enter the category name.")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    maxLengthTitle = Page._meta.get_field('title').max_length
    maxLengthURL = Page._meta.get_field('url').max_length

    title = forms.CharField(max_length=maxLengthTitle,
                           help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=maxLengthURL,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:

        model = Page
        exclude = ('category',)
