from django import forms
from .models import Comments, Post , Images

class NewPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['description','videofile', 'tags']

class NewCommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['comment']

class ImageForm(NewPostForm): #extending form
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(NewPostForm.Meta):
        fields = NewPostForm.Meta.fields + ['images',]

# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Image')    
#     class Meta:
#         model = Images
#         fields = ('image', )