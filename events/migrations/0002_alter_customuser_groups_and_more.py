from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('events', '0001_initial'),
    ]

    operations = [
        # Alter field groups on customuser
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(
                related_name='customuser_set',  # Updated related_name
                to='auth.Group',
                blank=True,
                help_text='The groups this user belongs to.',
                verbose_name='groups',
            ),
        ),
        # Alter field user_permissions on customuser
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(
                related_name='customuser_set',  # Updated related_name
                to='auth.Permission',
                blank=True,
                help_text='Specific permissions for this user.',
                verbose_name='user permissions',
            ),
        ),
        # Create model Event
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('category', models.CharField(max_length=50, blank=True, null=True)),
                ('image', models.ImageField(upload_to='event_images/', blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=models.CASCADE, to='auth.User')),
            ],
        ),
    ]
