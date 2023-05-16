from fulcrum.mixins import Findable, Deleteable, Createable, Historical, Searchable, Updateable, Media, Track, MediaCreateable
from . import BaseAPI


class Forms(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable, Historical):
    path = 'forms'

class Records(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable, Historical):
    path = 'records'


class Webhooks(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'webhooks'


class Photos(BaseAPI, Findable, Searchable, Media, MediaCreateable):
    path = 'photos'
    ext = 'jpg'
    sizes = ['thumbnail', 'large']
    media_upload_path = ''
    media_form_field_name = 'photo'
    default_content_type = 'image/jpeg'


class Signatures(BaseAPI, Findable, Searchable, Media, MediaCreateable):
    path = 'signatures'
    ext = 'png'
    sizes = ['thumbnail', 'large']
    media_upload_path = ''
    media_form_field_name = 'signature'
    default_content_type = 'image/png'


class Videos(BaseAPI, Findable, Searchable, Media, Track, MediaCreateable):
    path = 'videos'
    ext = 'mp4'
    sizes = ['small', 'medium']
    media_upload_path = '/upload'
    media_form_field_name = 'video'
    default_content_type = 'video/mp4'


class Audio(BaseAPI, Findable, Searchable, Media, Track, MediaCreateable):
    path = 'audio'
    ext = 'mp4'
    sizes = []
    media_upload_path = '/upload'
    media_form_field_name = 'audio'
    default_content_type = 'audio/mp3'


class Memberships(BaseAPI, Searchable):
    path = 'memberships'

    def change(self, resource_type, id, action, membership_ids):
        change = {
            'type': '{}_members'.format(resource_type),
            '{}_id'.format(resource_type): id,
            action: membership_ids
        }
        data = {'change': change}
        api_resp = self.client.call('post', 'memberships/change_permissions',
                                    data=data,
                                    extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Roles(BaseAPI, Searchable):
    path = 'roles'


class ChoiceLists(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'choice_lists'


class ClassificationSets(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'classification_sets'


class Projects(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'projects'


class Changesets(BaseAPI, Findable, Createable, Searchable, Updateable):
    path = 'changesets'

    def close(self, id):
        api_resp = api_resp = self.client.call('put', '{0}/{1}/close'.format(self.path, id))
        return api_resp


class ChildRecords(BaseAPI, Searchable):
    path = 'child_records'


class AuditLogs(BaseAPI, Searchable, Findable):
    path = 'audit_logs'


class Layers(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'layers'


class Authorizations(BaseAPI, Findable, Deleteable, Searchable, Updateable):
    path = 'authorizations'

    def regenerate(self, id):
        api_resp = self.client.call('post', '{}/{}/regenerate'.format(self.path, id))
        return api_resp
