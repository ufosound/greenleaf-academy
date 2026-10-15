from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок урока")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    # Новое поле для файла
    file = models.FileField(upload_to='lessons_files/', blank=True, null=True, verbose_name="Файл урока (PDF)")

    class Meta:
        ordering = ['order']
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions', verbose_name="Урок")
    text = models.TextField(verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"Вопрос для: {self.lesson.title}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    text = models.CharField(max_length=255, verbose_name="Вариант ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.text

class UserProgress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"