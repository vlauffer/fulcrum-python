from fulcrum.utils import is_string, generate_uuid

class Findable(object):
    def find(self, id, url_params=None):
        api_resp = self.client.call('get', '{0}/{1}'.format(self.path, id), url_params=url_params)
        return api_resp


class Deleteable(object):
    def delete(self, id):
        self.client.call('delete', '{0}/{1}'.format(self.path, id))


class Createable(object):
    def create(self, obj):
        api_resp = self.client.call('post', self.path, data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Searchable(object):
    def search(self, url_params=None):
        api_resp = self.client.call('get', self.path, url_params=url_params)
        return api_resp


class Updateable(object):
    def update(self, id, obj):
        api_resp = self.client.call('put', '{0}/{1}'.format(self.path, id), data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Media(object):
    def media(self, id, size='original'):
        if size == 'original':
            path = '{}/{}.{}'.format(self.path, id, self.ext)
        else:
            if not size in self.sizes:
                raise ValueError('Size {} not supported'.format(size))
            path = '{}/{}/{}.{}'.format(self.path, id, size, self.ext)

        api_resp = self.client.call('get', path, json_content=False)
        return api_resp


class Track(object):
    track_formats = {
        'json': 'json',
        'geojson': 'geojson',
        'gpx': 'gpx',
        'kml': 'kml',
        'geojson_points': 'geojson?type=points',
    }

    def track(self, id, format='json'):
        if not format in self.track_formats.keys():
            raise ValueError('Format {} not supported'.format(format))
        path = '{}/{}/track.{}'.format(self.path, id, self.track_formats[format])

        is_json_resp = format in ('json', 'geojson', 'geojson_points')

        api_resp = self.client.call('get', path, json_content=is_json_resp)
        return api_resp


class MediaCreateable(object):
    def create(self, media_or_path, content_type=None, access_key=None):
        if is_string(media_or_path):
            media = open(media_or_path, 'rb')
        else:
            media = media_or_path

        data = {
            '{}[access_key]'.format(self.media_form_field_name): access_key or generate_uuid()
        }

        files = {
            '{}[file]'.format(self.media_form_field_name): (media.name, media, content_type or self.default_content_type)
        }

        api_resp = self.client.call('post', self.path + self.media_upload_path, data=data, files=files)
        return api_resp
    
class PermissionChangable(object):
    def change(self, resource_type, id, action, object_ids):
        resource_type_string =  f'{resource_type}_members'
        id_prefix = f'{resource_type}_id'
        if self.path != 'memberships':
            resource_type_string = f'{self.path[:-1]}_{resource_type}'
            id_prefix = f'{self.path[:-1]}_id'
        change = {
            'type': resource_type_string,
            id_prefix: id,
            action: object_ids
        }
        data = {'change': change}
        api_resp = self.client.call('post', f'{self.path}/change_permissions',
                                    data=data,
                                    extra_headers={'Content-Type': 'application/json'})
        return api_resp
