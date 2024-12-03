from django.db import models

# Create your models here.
##Model de  Gerenciamentode vídeos
class Video(models.Model):
  title = models.CharField(max_length=255, unique=True, verbose_name="Título")
  description = models.TextField(verbose_name="Descrição")
  thumbnail = models.ImageField(upload_to="thumbnails/", verbose_name="Miniaturas")
#   video = models.FileField(upload_to="media/", verbose_name="Vídeo")
  slug =models.SlugField(max_length=100, unique=True)
  published_at = models.DateTimeField(verbose_name="Publicado em",null =True,  editable=False)
  is_published = models.BooleanField( default=False, verbose_name="Publicado")
  num_likes = models.IntegerField(default=0, verbose_name="número de curtidas", editable=False)
  num_viewa = models.IntegerField(default=0, verbose_name="número de vidualizações", editable=False)
  tags = models.ManyToManyField('Tag', verbose_name='Tags', related_name='videos')
 
  class Meta():
    verbose_name ="Vídeo" #Singular
    verbose_name_plural ="Vídeos" #Plural

  def __str__(self):
    return self.title

class VideoMedia(models.Model):
    class Status(models.TextChoices):
        UPLOADED_STARTED = 'UPLOADED_STARTED', 'Upload Iniciado'
        PROCESS_STARTED = 'PROCESSING_STARTED', 'Processamento Iniciado'
        PROCESS_FINISHED = 'PROCESSING_FINISHED', 'Processamento Finalizado'
        PROCESS_ERROR = 'PROCESSING_ERROR', 'Erro no Processamento'

    video_path = models.CharField(max_length=255, verbose_name='Vídeo')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED_STARTED, verbose_name='Status')
    video = models.OneToOneField('Video', on_delete=models.PROTECT, verbose_name='Vídeo', related_name='video_media')

    class Media:
        verbose_name = 'Mídia'
        verbose_name_plural = 'Mídias'


    def get_status_display(self):
        return VideoMedia.Status(self.status).label

   


  #  class Status(models.TextChoices):
  #     UPLOADED_STARTED = 'UPLOADED_STARTED','Upaload Iniciado'
  #     PROCESS_STARTED = 'PROCESS_STARTED','Processo Iniciado'
  #     PROCESS_FINISHED = 'PROCESS_FINISHED','Proecess Finalizado'
  #     PROCESS_ERROR = 'PROCESS_ERROR','Erro no processo'
   
  #  videoPath = models.CharField(max_length=255, verbose_name='Video')
  #  status = models.CharField(max_length=20, choices= Status.choices, default=Status.UPLOADED_STARTED, verbose_name='Status')
  #  video = models.OneToOneField('Video', on_delete=models.PROTECT, verbose_name="vídeo", related_name='video_media')

   

  #  def get_status_display(self):
  #     return VideoMedia.Status(self.status).label
      
  #  class Media:
  #     verbose_name = 'Mídia'
  #     verbose_name_plural = 'Mídias'


class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True, verbose_name='Nome')
  class Meta():
    verbose_name ="Tag" #Singular
    verbose_name_plural ="Tags" #Plural


  def __str__(self):
    return self.name
