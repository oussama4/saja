# Generated by Django 2.2.12 on 2020-05-14 20:29

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.TextField(blank=True, help_text='Texte pour décrire la page', null=True)),
                ('body', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(features=['h2', 'h4', 'bold', 'italic', 'ol', 'ul', 'link'], help_text='une paragraphe', ion='doc-full')), ('title_and_paragraph', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Titre de paragraphe', required=True)), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'], help_text='le paragraphe', required=True))]))], verbose_name='corps')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]