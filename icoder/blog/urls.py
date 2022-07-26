from django.contrib import admin
from django.urls import path 
from . import views
from icoder.settings import DEBUG, STATIC_URL, STATICFILES_DIRS
from django.conf.urls.static import static

urlpatterns = [

    path('postComment', views.postComment, name="postComment"),
    path('', views.blogHome, name="bloghome"),
    path('<str:slug>', views.blogPost, name="blogPost"),
    path('upload/', views.upload, name = 'upload-post'),
    path('update/<int:post_id>', views.update_post, name='update'),
    path('delete/<int:post_id>', views.delete_post, name='delete'),
    path('edit_note/', views.edit_note, name="EditNote"),
    path('delete_note/', views.delete_note, name="DeleteNote"),
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATICFILES_DIRS)

    