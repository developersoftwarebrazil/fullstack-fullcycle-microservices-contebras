import traceback
from typing import Any
from django.contrib import admin,messages
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render
from django.urls import path, reverse
from django.http import HttpRequest, JsonResponse
from django.urls.resolvers import URLPattern
from django.utils.html import format_html
from contebras_core.models import Video, Tag

from django.contrib.auth.admin import csrf_protect_m

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published', 'num_likes', 'num_views', 'redirect_to_upload', )
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ["title"]}


    def get_urls(self):
        urls =  super().get_urls()
        custom_urls = [
            path('<int:id>/upload-video', self.upload_video, name='core_video_upload')
        ]
        return custom_urls + urls

    def upload_video(self, request, id):
        return render(request, 'admin/core/upload_video.html')

    # def get_readonly_fields(self, request: HttpRequest, obj: Any | None) -> list[str]:
    #     return ['video_status','is_published', 'published_at', 'num_likes', 'num_views', 'author'] if not obj else [
    #         'video_status','published_at', 'num_likes', 'num_views', 'author'
    #     ]

    # def video_status(self, obj: Video) -> str:
    #     return obj.get_video_status_display()

    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             '<int:id>/upload-video', 
    #             self.admin_site.admin_view(self.upload_video_view), 
    #             name='core_video_upload'
    #         ),
    #         path(
    #             '<int:id>/upload-video/finish', 
    #             self.admin_site.admin_view(self.finish_upload_video_view), 
    #             name='core_video_upload_finish'
    #         ),
    #     ]
    #     return custom_urls + urls
    
    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         obj.author = request.user
    #     super().save_model(request, obj, form, change)

    # def redirect_to_upload(self, obj: Video):
    #     url = reverse('admin:core_video_upload', args=[obj.id])
    #     return format_html(f'<a href="{url}">Upload</a>')

    # redirect_to_upload.short_description = 'Upload'
    
    # @csrf_protect_m
    # def upload_video_view(self, request, id):

    #     str_id = str(id)
        
    #     if request.method == 'POST':
    #         return self._do_upload_video_chunks(request, id)
        
    #     try:
    #         video = create_video_service_factory().find_video(id)
    #         context = dict(
    #             self.admin_site.each_context(request), # Include common variables for rendering the admin template.
    #             opts=self.model._meta,
    #             id=id,
    #             video=video,
    #             video_media=video.video_media if hasattr(video, 'video_media') else None,
    #             has_view_permission=True
    #         )
    #         return render(request, 'admin/core/upload_video.html', context)
    #     except Video.DoesNotExist:
    #          return self._get_obj_does_not_exist_redirect(
    #                 request, self.opts, str_id
    #         )

    # def _do_upload_video_chunks(self, request: HttpRequest, id: int) -> Any:
    #     form = VideoChunkUploadForm(request.POST, request.FILES)

    #     if not form.is_valid():
    #         return JsonResponse({'error': form.errors}, status=400)

    #     try:
    #         create_video_service_factory().process_upload(
    #             video_id=id,
    #             chunk_index=form.cleaned_data['chunkIndex'],
    #             chunk=form.cleaned_data['chunk'].read()
    #         )
    #     except Video.DoesNotExist:
    #         return JsonResponse({'error': 'Vídeo não encontrado.'}, status=404)
    #     except Exception as e:
    #         traceback.print_exc()
    #         return JsonResponse({'error': str(e)}, status=500)

    #     return JsonResponse({}, status=204)

    # def finish_upload_video_view(self, request, id):
    #     if request.method != 'POST':
    #         return JsonResponse({'error': 'Método não permitido.'}, status=405)
        
    #     form = VideoChunkFinishUploadForm(request.POST)

    #     if not form.is_valid():
    #         return JsonResponse({'error': form.errors}, status=400)
        
    #     try:
    #         create_video_service_factory().finalize_upload(id, form.cleaned_data['totalChunks'])
    #     except Video.DoesNotExist:
    #         return JsonResponse({'error': 'Vídeo não encontrado.'}, status=404)
    #     except (VideoMediaNotExistsException, VideoMediaInvalidStatusException, VideoChunkUploadException) as e:
    #         return JsonResponse({'error': str(e)}, status=400)

    #     self.message_user(request, 'Upload realizado com sucesso.', messages.SUCCESS)

    #     return JsonResponse({}, status=204)

admin.site.site_header = 'Painel Administrativo da Escola Contebras'

admin.site.register(Video)
admin.site.register(Tag)



# from .models import Student, Course, Classroom, Registration, Video, Tag


# @admin.register(Video)
# class VideoAdmin(admin.ModelAdmin):
#      list_display = ('title', 'description')
#      search_fields = ('title', 'description')

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# # Admin de Aluno
# @admin.register(Student)
# class AdminStudent(admin.ModelAdmin):
#     list_display = ('studentName', 'studentEmail')
#     search_fields = ('studentName', 'studentEmail')


# # Admin de Curso
# @admin.register(Course)
# class AdminCourse(admin.ModelAdmin):
#     list_display = ('titleCourse', 'descripton')
#     search_fields = ('titleCourse',)

# # Admin de Turma
# @admin.register(Classroom)
# class AdminClassroom(admin.ModelAdmin):
#     list_display = ('classroomName', 'course')
#     search_fields = ('classroomName', 'course__titleCourse')

# # Admin de Matricula
# @admin.register(Registration)
# class AdminRegistarion(admin.ModelAdmin):
#     list_display = ('registrationStudent', 'registrationClassroom', 'registrationDate')
#     search_fields = ('registrationStuden__classroomName ', 'registrationClassroom__classroomName ')
#     list_filter = ('registrationDate',)

# # # Admin de VídeoCurso
# # @admin.register(VideoCurso)
# # class VideoCursoAdmin(admin.ModelAdmin):
# #     list_display = ('titulo', 'curso', 'url')
# #     search_fields = ('titulo', 'curso__titulo')







# # from django.contrib import admin
# # from contebras_core.models import Video,Tag, Course, Student,ClassroomStudent

# # # Register your models here.
# # admin.site.register(Course)
# # admin.site.register(Student)
# # admin.site.register(ClassroomStudent)
# # admin.site.register(Tag)
# # admin.site.register(Video)

