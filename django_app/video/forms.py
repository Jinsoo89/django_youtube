from django import forms


class KeywordForm(forms.Form):
    keyword = forms.CharField(max_length=50, label="keyword")


class ResultForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(max_length=300)
    # url = models.URLField()
    youtube_id = forms.CharField(max_length=100)
    published_date = forms.DateTimeField()