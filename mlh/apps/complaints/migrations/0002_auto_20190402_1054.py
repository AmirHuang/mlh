# Generated by Django 2.2 on 2019-04-02 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('complaints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaintmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='complaintlikemodel',
            name='complaint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complaints.ComplaintModel', verbose_name='所属吐槽'),
        ),
        migrations.AddField(
            model_name='complaintlikemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='complaintcommentlikemodel',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complaints.CommentModel', verbose_name='所属吐槽'),
        ),
        migrations.AddField(
            model_name='complaintcommentlikemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='complaintcollectionmodel',
            name='complaint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complaints.ComplaintModel', verbose_name='所属吐槽'),
        ),
        migrations.AddField(
            model_name='complaintcollectionmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_comments', to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='complaint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='complaints.ComplaintModel', verbose_name='所属吐槽'),
        ),
        migrations.AlterUniqueTogether(
            name='complaintlikemodel',
            unique_together={('user', 'complaint')},
        ),
        migrations.AlterUniqueTogether(
            name='complaintcommentlikemodel',
            unique_together={('user', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='complaintcollectionmodel',
            unique_together={('user', 'complaint')},
        ),
    ]
