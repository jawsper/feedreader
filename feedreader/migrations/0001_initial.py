# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('feedreader_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('xmlUrl', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('htmlUrl', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('faviconUrl', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('lastPubDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('lastUpdated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('lastStatus', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('feedreader', ['Feed'])

        # Adding model 'Outline'
        db.create_table('feedreader_outline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedreader.Outline'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedreader.Feed'], null=True, blank=True)),
            ('sort_position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sort_order_asc', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_only_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('folder_opened', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('feedreader', ['Outline'])

        # Adding model 'Post'
        db.create_table('feedreader_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedreader.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('pubDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('guid_is_permalink', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('feedreader', ['Post'])

        # Adding model 'UserPost'
        db.create_table('feedreader_userpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedreader.Post'])),
            ('starred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('feedreader', ['UserPost'])

        # Adding unique constraint on 'UserPost', fields ['user', 'post']
        db.create_unique('feedreader_userpost', ['user_id', 'post_id'])

        # Adding model 'ConfigStore'
        db.create_table('feedreader_configstore', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('feedreader', ['ConfigStore'])

        # Adding unique constraint on 'ConfigStore', fields ['key', 'user']
        db.create_unique('feedreader_configstore', ['key', 'user_id'])

        # Adding model 'UserToken'
        db.create_table('feedreader_usertoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('expire', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('feedreader', ['UserToken'])


    def backwards(self, orm):
        # Removing unique constraint on 'ConfigStore', fields ['key', 'user']
        db.delete_unique('feedreader_configstore', ['key', 'user_id'])

        # Removing unique constraint on 'UserPost', fields ['user', 'post']
        db.delete_unique('feedreader_userpost', ['user_id', 'post_id'])

        # Deleting model 'Feed'
        db.delete_table('feedreader_feed')

        # Deleting model 'Outline'
        db.delete_table('feedreader_outline')

        # Deleting model 'Post'
        db.delete_table('feedreader_post')

        # Deleting model 'UserPost'
        db.delete_table('feedreader_userpost')

        # Deleting model 'ConfigStore'
        db.delete_table('feedreader_configstore')

        # Deleting model 'UserToken'
        db.delete_table('feedreader_usertoken')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'feedreader.configstore': {
            'Meta': {'unique_together': "(('key', 'user'),)", 'object_name': 'ConfigStore'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feedreader.feed': {
            'Meta': {'object_name': 'Feed'},
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'faviconUrl': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'htmlUrl': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastPubDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastStatus': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'lastUpdated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'xmlUrl': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'feedreader.outline': {
            'Meta': {'object_name': 'Outline'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedreader.Feed']", 'null': 'True', 'blank': 'True'}),
            'folder_opened': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedreader.Outline']", 'null': 'True', 'blank': 'True'}),
            'show_only_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sort_order_asc': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sort_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'feedreader.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedreader.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'guid_is_permalink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'feedreader.userpost': {
            'Meta': {'unique_together': "(('user', 'post'),)", 'object_name': 'UserPost'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedreader.Post']"}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'starred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'feedreader.usertoken': {
            'Meta': {'object_name': 'UserToken'},
            'expire': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['feedreader']