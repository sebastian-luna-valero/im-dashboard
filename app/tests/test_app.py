import sys

sys.path.append('..')
sys.path.append('.')

import unittest
import json
import defusedxml.ElementTree as etree
from app import create_app
from urllib.parse import urlparse
from mock import patch, MagicMock


class IMDashboardTests(unittest.TestCase):

    oauth = MagicMock()

    def setUp(self):
        self.app = create_app(self.oauth)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    @staticmethod
    def get_response(url, params=None, **kwargs):
        resp = MagicMock()
        parts = urlparse(url)
        url = parts[2]
        # params = parts[4]

        resp.status_code = 404
        resp.ok = False

        if url == "/im/infrastructures":
            print(params)
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"uri-list": [{"uri": "http://server.com/im/infrastructures/infid"}]}
        elif url == "/im/infrastructures/infid/state":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"state": {"state": "configured", "vm_states": {"0": "configured"}}}
        elif url == "/im/infrastructures/infid/vms/0":
            resp.ok = True
            resp.status_code = 200
            resp.text = "system front (cpu.count = 1 and memory.size = 512 MiB)"
            radl = {"class": "system",
                    "cpu.arch": "x86_64",
                    "cpu.count_min": 1,
                    "disk.0.image.url": "one://server.com/id",
                    "disk.0.os.name": "linux",
                    "id": "front",
                    "state": "configured",
                    "disk.0.os.credentials.username": "user",
                    "disk.0.os.credentials.password": "pass",
                    "memory.size_min": 536870912,
                    "net_interface.0.connection": "publica",
                    "net_interface.0.ip": "10.10.10.10",
                    "provider.type": "OpenNebula",
                    "provider.host": "server.com"}
            resp.json.return_value = {"radl": [radl]}
        elif url == "/im/infrastructures/infid/vms/0/stop":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures/infid/tosca":
            resp.ok = True
            resp.status_code = 200
            resp.text = """
                           metadata:
                             tabs:
                                Tab1:
                                  - param1:
                                      reconfigure: true
                             template_name: VM
                             filename: simple-node-disk.yml
                             childs:
                               - users.yml
                           topology_template:
                             inputs:
                               num_cpus:
                                 type: integer
                                 default: 4
                               param1:
                                 type: string
                                 description: Param1 description
                                 default: ''
                             node_templates:
                                simple_node:
                                        type: tosca.nodes.indigo.Compute"""
        elif url == "/im/infrastructures/infid/contmsg":
            resp.ok = True
            resp.status_code = 200
            resp.text = "CONT_MSG"
        elif url == "/im/infrastructures/infid/vms/0/contmsg":
            resp.ok = True
            resp.status_code = 200
            resp.text = "VM_CONT_MSG"
        elif url == "/im/infrastructures/infid/outputs":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"outputs": {"key": "value", "key2": "http://server.com"}}
        elif url == "/im/infrastructures/infid/radl":
            resp.ok = True
            resp.status_code = 200
            resp.text = "description desc (name = 'infname')\n system wn ()\nsystem front ()"
        elif url == "/im/clouds/credid/images":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"images": [{"uri": "one://server/imageid", "name": "imagename"}]}
        elif url == "/im/clouds/credid/quotas":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"quotas": {"cores": {"used": 1, "limit": 10},
                                                 "ram": {"used": 1, "limit": 10},
                                                 "instances": {"used": 1, "limit": 10},
                                                 "floating_ips": {"used": 1, "limit": 10},
                                                 "security_groups": {"used": 1, "limit": 10},
                                                 "volumes": {"used": 1, "limit": 10},
                                                 "volume_storage": {"used": 1, "limit": 10}}}
        elif url == "/im/stats":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"stats": [{'creation_date': '2022-03-07 13:16:14',
                                                 'tosca_name': 'kubernetes',
                                                 'vm_count': 2,
                                                 'cpu_count': 4,
                                                 'memory_size': 1024,
                                                 'cloud_type': 'OSCAR',
                                                 'cloud_host': 'sharp-elbakyan5.im.grycap.net',
                                                 'hybrid': False,
                                                 'im_user': '__OPENID__mcaballer',
                                                 'inf_id': '1',
                                                 'last_date': '2022-03-23'}]}
        elif url == "/im/infrastructures/infid/authorization":
            resp.ok = True
            resp.status_code = 200
            resp.text = "user1\nuser2"
        elif url == "/im/infrastructures/infid/data":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {'data': '{"some": "value"}'}

        return resp

    @staticmethod
    def put_response(url, params=None, **kwargs):
        resp = MagicMock()
        parts = urlparse(url)
        url = parts[2]

        resp.status_code = 404
        resp.ok = False

        if url == "/im/infrastructures/infid/vms/0/stop":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures/infid/reconfigure":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures/infid/stop":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures/infid/vms/0":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures":
            resp.ok = True
            resp.status_code = 200
            resp.text = "http://server.com/im/infrastructures/infid"

        return resp

    @staticmethod
    def delete_response(url, params=None, **kwargs):
        resp = MagicMock()
        parts = urlparse(url)
        url = parts[2]

        resp.status_code = 404
        resp.ok = False

        if url == "/im/infrastructures/infid/vms/0":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures/infid/vms/1,2":
            resp.ok = True
            resp.status_code = 200
        elif url == "/im/infrastructures/infid":
            resp.ok = True
            resp.status_code = 200

        return resp

    def post_response(self, url, params=None, **kwargs):
        resp = MagicMock()
        parts = urlparse(url)
        url = parts[2]
        query = parts[4]

        resp.status_code = 404
        resp.ok = False

        if url == "/im/infrastructures" and "dry_run=1" in query:
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {
                "ost1": {
                    "cloudType": "OpenStack",
                    "cloudEndpoint": "http://openstack.example.com:5000",
                    "compute": [
                        {
                            "cpuCores": 2,
                            "memoryInMegabytes": 4096,
                            "diskSizeInGigabytes": 20,
                            "publicIP": 1,
                        },
                        {
                            "cpuCores": 1,
                            "memoryInMegabytes": 2048,
                            "diskSizeInGigabytes": 10,
                        },
                    ],
                    "storage": [{"sizeInGigabytes": 100}],
                }
            }
        elif url == "/im/infrastructures":
            resp.ok = True
            resp.status_code = 200
            self.assertTrue("IMAGE_NAME" in kwargs["data"] or "appdbimage" in kwargs["data"])
            self.assertIn("default: 4", kwargs["data"])
        elif url == "/im/infrastructures/infid":
            resp.ok = True
            resp.status_code = 200
            resp.json.return_value = {"uri-list": [{"uri": "VM_URI"}]}
        elif url == "/im/infrastructures/infid/authorization":
            resp.ok = True
            resp.status_code = 200
            resp.text = ""

        return resp

    def login(self, avatar):
        self.oauth.session.authorized = True
        self.oauth.session.token = {'expires_in': 500, 'access_token': 'token'}
        account_info = MagicMock()
        account_info.ok = True
        account_info.json.return_value = {"sub": "userid", "name": "username",
                                          "eduperson_entitlement": ["urn:mace:egi.eu:group:VO_NAME:role=r#aai.egi.eu",
                                                                    "urn:mace:egi.eu:group:vo:role=r#aai.egi.eu"]}
        self.oauth.session.get.return_value = account_info
        avatar.return_value = ""
        return self.client.get('/')

    def test_index_with_no_login(self):
        self.oauth.session.authorized = False
        res = self.client.get('/')
        self.assertEqual(302, res.status_code)
        self.assertIn('/login', res.headers['location'])

    @patch("app.utils.avatar")
    def test_index(self, avatar):
        res = self.login(avatar)
        self.assertEqual(200, res.status_code)

    @patch("app.utils.avatar")
    def test_settings(self, avatar):
        self.login(avatar)
        res = self.client.get('/settings')
        self.assertEqual(200, res.status_code)
        self.assertIn(b"https://appsgrycap.i3m.upv.es:31443/im", res.data)

    @patch("app.db_cred.DBCredentials.get_creds")
    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_infrastructures(self, avatar, get, user_data, get_creds):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get_creds.return_value = []
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/infrastructures')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'infid', res.data)
        self.assertIn(b'infname', res.data)
        self.assertIn(b'OpenNebula', res.data)
        self.assertIn(b'server.com', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.put')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_manageinf_stop(self, flash, avatar, put, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        put.side_effect = self.put_response
        self.login(avatar)
        res = self.client.post('/manage_inf/infid/stop')
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0],
                         ("Operation 'stop' successfully made on Infrastructure ID: infid", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.post')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_manageinf_change_user(self, flash, avatar, post, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        post.side_effect = self.post_response
        self.login(avatar)
        params = {"token": "token"}
        res = self.client.post('/manage_inf/infid/change_user', data=params)
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0],
                         ("Infrastructure owner successfully changed.", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.put')
    @patch('requests.get')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_manageinf_migrate(self, flash, avatar, get, put, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        put.side_effect = self.put_response
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.post('/manage_inf/infid/migrate', data={"new_im_url": "http://newim.com/im"})
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0],
                         ("Infrastructure successfully migrated to http://server.com/im/infrastructures/infid.",
                          'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_vm_info(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/vminfo?infId=infid&vmId=0')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Username: user', res.data)
        self.assertIn(b'Password: pass', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.put')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_managevm_stop(self, flash, avatar, put, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        put.side_effect = self.put_response
        self.login(avatar)
        res = self.client.post('/managevm/stop/infid/0')
        self.assertEqual(302, res.status_code)
        self.assertIn('/vminfo?infId=infid&vmId=0', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Operation 'stop' successfully made on VM ID: 0", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.delete')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_managevm_delete(self, flash, avatar, delete, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        delete.side_effect = self.delete_response
        self.login(avatar)
        res = self.client.post('/managevm/terminate/infid/0')
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Operation 'terminate' successfully made on VM ID: 0",
                                                      'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch('requests.put')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_managevm_resize(self, flash, avatar, put, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        put.side_effect = self.put_response
        get.side_effect = self.get_response
        self.login(avatar)
        params = {'cpu': '4',
                  'memory': '4',
                  'system_name': 'front'
                  }
        res = self.client.post('/managevm/resize/infid/0', data=params)
        self.assertEqual(302, res.status_code)
        self.assertIn('/vminfo?infId=infid&vmId=0', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Operation 'resize' successfully made on VM ID: 0", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.put')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_reconfigure(self, flash, avatar, put, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        put.side_effect = self.put_response
        self.login(avatar)
        res = self.client.post('/manage_inf/infid/reconfigure')
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Reconfiguration process successfuly started.", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_template(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/template/infid')
        self.assertEqual(200, res.status_code)
        expected = b"node_templates:\n    simple_node:\n      type: tosca.nodes.indigo.Compute"
        self.assertIn(expected, res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_log(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/log/infid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'CONT_MSG', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_vm_log(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/vmlog/infid/0')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'VM_CONT_MSG', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_outputs(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/outputs/infid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'key', res.data)
        self.assertIn(b'key2', res.data)
        self.assertIn(b'value', res.data)
        self.assertIn(b"<a href='http://server.com' target='_blank'>http://server.com</a>", res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.delete')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_delete(self, flash, avatar, delete, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        delete.side_effect = self.delete_response
        self.login(avatar)
        res = self.client.post('/manage_inf/infid/delete')
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Infrastructure 'infid' successfuly deleted.", 'success'))

    @patch("app.utils.avatar")
    @patch("app.db_cred.DBCredentials.get_creds")
    @patch('requests.get')
    def test_configure(self, get, get_creds, avatar):
        self.login(avatar)
        get.side_effect = self.get_response
        res = self.client.get('/configure?selected_tosca=simple-node-disk.yml')
        self.assertEqual(200, res.status_code)
        self.assertIn(b"Select Optional Features:", res.data)

        get_creds.return_value = [{"id": "credid", "type": "fedcloud", "host": "site_url",
                                   "vo": "voname", "enabled": True},
                                  {"id": "credid1", "type": "OpenStack", "host": "site_url1",
                                   "tenant_id": "tenid", "enabled": True}]
        res = self.client.get('/configure?selected_tosca=simple-node-disk.yml&childs=users.yml')
        self.assertEqual(200, res.status_code)
        self.assertIn(b"Deploy a compute node getting the IP and SSH credentials to access via ssh", res.data)

        res = self.client.get('/configure?selected_tosca=simple-node-disk.yml&inf_id=infid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'<option selected value="4">4</option>', res.data)

    @patch("app.utils.avatar")
    @patch("app.appdb.get_sites")
    def test_sites(self, get_sites, avatar):
        self.login(avatar)
        get_sites.return_value = {"SITE_NAME": {"url": "URL", "state": "", "id": ""},
                                  "SITE2": {"url": "URL2", "state": "CRITICAL", "id": ""}}
        res = self.client.get('/sites/vo')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'<option name="selectedSite" value=URL>SITE_NAME</option>', res.data)
        self.assertIn(b'<option name="selectedSite" value=static_site_url>static_site_name</option>', res.data)
        self.assertIn(b'<option name="selectedSite" value=URL2>SITE2 (WARNING: CRITICAL state!)</option>', res.data)

    @patch("app.utils.avatar")
    @patch("app.utils.getUserAuthData")
    @patch("app.utils.get_site_info")
    @patch("app.appdb.get_images")
    @patch('requests.get')
    def test_images(self, get, get_images, get_site_info, user_data, avatar):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        get_site_info.return_value = ({"id": "id"}, "", "vo_name")

        res = self.client.get('/images/credid?local=1')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'<option name="selectedSiteImage" value=one://server/imageid>imagename</option>', res.data)

        get_images.return_value = [("IMAGE_NAME", "IMAGE")]
        res = self.client.get('/images/credid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'<option name="selectedImage" value=IMAGE>IMAGE_NAME</option>', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.post')
    @patch("app.utils.avatar")
    @patch("app.utils.get_site_info")
    @patch("app.db_cred.DBCredentials.get_cred")
    @patch("app.ssh_key.SSHKey.get_ssh_keys")
    @patch("app.flash")
    def test_submit(self, flash, get_ssh_keys, get_cred, get_site_info, avatar, post, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        post.side_effect = self.post_response
        get_cred.return_value = {"id": "credid", "type": "fedcloud"}
        get_ssh_keys.return_value = [(1, "desc", "ssh-rsa AAAAB3NzaC...")]
        get_site_info.return_value = {}, "", "vo"
        self.login(avatar)
        params = {'extra_opts.selectedImage': '',
                  'extra_opts.selectedSiteImage': 'IMAGE_NAME',
                  'extra_opts.selectedCred': 'credid',
                  'num_cpus': '4',
                  'ports': '22,80,443',
                  'storage_size': '0 GB',
                  'mount_path': '/mnt/disk',
                  'infra_name': 'some_infra'
                  }
        res = self.client.post('/submit?template=simple-node-disk.yml', data=params)
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_count, 0)

    @patch('app.utils.get_site_info')
    @patch("app.utils.getUserAuthData")
    @patch('requests.post')
    @patch("app.utils.avatar")
    @patch("app.db_cred.DBCredentials.get_cred")
    @patch("app.flash")
    def test_submit2(self, flash, get_cred, avatar, post, user_data, get_site_info):
        site = {"name": "SITE", "networks": {"vo": {"public": "pub_id", "private": "priv_id"}}}
        get_site_info.return_value = site, None, "vo"
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        post.side_effect = self.post_response
        get_cred.return_value = {"id": "credid", "type": "fedcloud", "vo": "vo"}
        self.login(avatar)
        params = {'extra_opts.selectedImage': 'appdbimage',
                  'extra_opts.selectedSiteImage': '',
                  'extra_opts.selectedCred': 'credid',
                  'num_cpus': '4',
                  'ports': '22,80,443',
                  'storage_size': '0 GB',
                  'mount_path': '/mnt/disk',
                  'infra_name': 'some_infra'}
        res = self.client.post('/submit?template=simple-node-disk.yml', data=params)
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_count, 0)

    @patch("app.utils.getUserAuthData")
    @patch('requests.post')
    @patch("app.utils.avatar")
    @patch("app.utils.get_site_info")
    @patch("app.db_cred.DBCredentials.get_cred")
    @patch("app.flash")
    def test_submit_tosca(self, flash, get_cred, get_site_info, avatar, post, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        post.side_effect = self.post_response
        get_cred.return_value = {"id": "credid", "type": "fedcloud"}
        get_site_info.return_value = {}, "", "vo"
        self.login(avatar)
        params = {'extra_opts.selectedImage': '',
                  'extra_opts.selectedSiteImage': 'IMAGE_NAME',
                  'extra_opts.selectedCred': 'credid',
                  'infra_name': 'some_infra',
                  'num_cpus': '4',
                  'tosca_url': 'https://raw.githubusercontent.com/grycap/tosca/main/templates/simple-node-disk.yml'
                  }
        res = self.client.post('/submit?template=tosca.yml', data=params)
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_count, 0)

    @patch("app.utils.avatar")
    @patch("app.db_cred.DBCredentials.get_creds")
    @patch("app.appdb.get_sites")
    @patch("app.appdb.get_project_ids")
    def test_manage_creds(self, get_project_ids, get_sites, get_creds, avatar):
        self.login(avatar)
        get_project_ids.return_value = {}
        get_sites.return_value = {"SITE_NAME": {"url": "URL", "state": "", "id": ""},
                                  "SITE2": {"url": "URL2", "state": "CRITICAL", "id": ""}}
        get_creds.return_value = [{"id": "credid", "type": "fedcloud", "host": "site_url", "project_id": "project"}]
        res = self.client.get('/manage_creds')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'credid', res.data)
        self.assertIn(b'site_url', res.data)
        self.assertIn(b'fedcloudRow.png', res.data)

        res = self.client.get('/manage_creds?json=1')
        self.assertEqual(200, res.status_code)
        self.assertEqual(json.loads(res.data), [{"id": "credid", "type": "fedcloud", "host": "site_url",
                                                 "project_id": "project"}])

    @patch("app.utils.avatar")
    @patch("app.db_cred.DBCredentials.get_cred")
    @patch("app.db_cred.DBCredentials.write_creds")
    @patch("app.flash")
    def test_write_creds(self, flash, write_creds, get_cred, avatar):
        self.login(avatar)
        get_cred.return_value = {"id": "credid", "type": "OpenNebula", "host": "SITE_URL",
                                 "username": "USER", "password": "PASS"}
        res = self.client.get('/write_creds?cred_type=OpenNebula&cred_id=')
        self.assertEqual(200, res.status_code)
        self.assertNotIn(b'site_url', res.data)

        res = self.client.get('/write_creds?cred_id=credid&cred_type=OpenNebula')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'SITE_URL', res.data)
        self.assertIn(b'USER', res.data)

        res = self.client.post('/write_creds?cred_id=credid&cred_type=OpenNebula', data={"host": "SITE_URL2",
                                                                                         "id": "credid",
                                                                                         "type": "OpenNebula"})
        self.assertEqual(302, res.status_code)
        self.assertIn('/manage_creds', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Credentials successfully written!", 'success'))
        self.assertEqual(write_creds.call_args_list[0][0], ('credid', 'userid', {'host': 'SITE_URL2',
                                                            'id': 'credid', 'type': "OpenNebula"}, False))

        res = self.client.post('/write_creds?cred_id=&cred_type=OpenNebula', data={"host": "SITE_URL3",
                                                                                   "id": "credid",
                                                                                   "type": "OpenNebula"})
        self.assertEqual(302, res.status_code)
        self.assertIn('/manage_creds', res.headers['location'])
        self.assertEqual(flash.call_args_list[1][0], ("Credentials successfully written!", 'success'))
        self.assertEqual(write_creds.call_args_list[1][0], ('credid', 'userid', {'host': 'SITE_URL3',
                                                                                 'id': 'credid',
                                                                                 'type': 'OpenNebula'}, True))

    @patch("app.utils.avatar")
    @patch("app.db_cred.DBCredentials.delete_cred")
    @patch("app.flash")
    def test_delete_creds(self, flash, delete_cred, avatar):
        self.login(avatar)
        delete_cred.return_value = True
        res = self.client.get('/delete_creds?service_id=SERVICE_ID')
        self.assertEqual(302, res.status_code)
        self.assertIn('/manage_creds', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("Credentials successfully deleted!", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_addresources_get(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/addresources/infid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'wn', res.data)
        self.assertIn(b'front', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch('requests.post')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_addresources(self, flash, avatar, post, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        post.side_effect = self.post_response
        self.login(avatar)
        res = self.client.post('/addresources/infid', data={"wn_num": "1"})
        self.assertEqual(302, res.status_code)
        self.assertEqual(flash.call_args_list[0][0], ("1 nodes added successfully", 'success'))

    @patch("app.utils.avatar")
    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch('requests.post')
    def test_quotas(self, post, get, user_data, avatar):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        post.side_effect = self.post_response

        self.login(avatar)

        res = self.client.get('/usage/credid?template=simple-node-disk.yml')
        self.assertEqual(200, res.status_code)
        expected_res = {"cores": {"used": 1, "limit": 10, "touse": 3},
                        "ram": {"used": 1, "limit": 10, "touse": 6},
                        "instances": {"used": 1, "limit": 10, "touse": 2},
                        "floating_ips": {"used": 1, "limit": 10, "touse": 1},
                        "security_groups": {"used": 1, "limit": 10, "touse": 3},
                        "volumes": {"used": 1, "limit": 10, "touse": 1},
                        "volume_storage": {"used": 1, "limit": 10, "touse": 100}}
        self.assertEqual(expected_res, json.loads(res.data))

    @patch("app.utils.avatar")
    @patch("app.utils.getIMUserAuthData")
    @patch('requests.get')
    @patch("app.utils.getCachedSiteList")
    def test_stats(self, get_sites, get, user_data, avatar):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        get_sites.return_value = {"SITE_NAME": {"url": "URL", "state": "", "id": "", "name": ""},
                                  "SITE2": {"url": "URL2", "state": "CRITICAL", "id": "", "name": ""}}
        res = self.client.get('/stats')
        self.assertEqual(200, res.status_code)
        self.assertNotIn(b'Error Getting Stats:', res.data)
        self.assertIn(b'clouds.push("sharp-elbakyan5.im.grycap.net");', res.data)
        self.assertIn(b'labels.push("2022-03-07 13:16:14");', res.data)
        self.assertIn(b'const infs = [0, 1, 0];', res.data)
        self.assertIn(b'const vms = [0, 2, 0];', res.data)

    @patch("app.utils.avatar")
    @patch("app.ssh_key.SSHKey.get_ssh_keys")
    def test_get_ssh_keys(self, get_ssh_keys, avatar):
        self.login(avatar)
        get_ssh_keys.return_value = [(1, "desc", "ssh-rsa AAAAB3NzaC...")]
        res = self.client.get('/ssh_keys')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'ssh-rsa AAAAB3NzaC...', res.data)

    @patch("app.utils.avatar")
    @patch("app.ssh_key.SSHKey.write_ssh_key")
    @patch("app.flash")
    def test_write_ssh_key(self, flash, write_ssh_key, avatar):
        self.login(avatar)
        key = ("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD2581vX45pELFhzX7j5f8G3luuKU00IXNYYPm4kWlC/bS8Do73LjJkSdJ/ETEzA"
               "lq99DBqehqmbFPa5OgRBqZmM/W278DimwMe8Alq/0droT9KlrrIetR42Q7ODGQq7+Z0plcy4J8R4HNVLQ4zSACIVXGjBhf9Ruii1R"
               "R139qEzz3v0DlLRdj+p4Y7o4qKkxFvZwVMsXboasGMZQoc1GRAZlNq7sCQr2yUrneh43Id1dRhqEgPWjPzzi9UXUbeXvKsqx0gsGr"
               "+ttuEqy3SM2ZBuhD6xrpAUGrr0TrJBJnVVBKL31zFSu6GcDtVyjoYGJhM/vU9VuBrUHO+qYIrcGP7VaPSOgTSj7V3OLD7pp8kYmFP"
               "vLKleDSI/eiKO0nH/J6W2mGa1J6FDFaIIsLIyERdgakjvrkecfv/YfqPWkUGp1xnzNugkOug1ZMQHfuSs7Ag+kVP3TDPQoAo8u2Yy"
               "EwbLK/vVSFlTe5eaotfCmiltVu3UaPYM8QylCCTW7QCncE= micafer@jonsu")
        res = self.client.post('/write_ssh_key', data={'sshkey': key, 'desc': 'desc'})
        self.assertEqual(302, res.status_code)
        self.assertIn('/ssh_key', res.headers['location'])
        self.assertLessEqual(flash.call_count, 0)

    @patch("app.utils.avatar")
    @patch("app.ssh_key.SSHKey.delete_ssh_key")
    @patch("app.flash")
    def test_delete_ssh_key(self, flash, delete_ssh_key, avatar):
        self.login(avatar)
        res = self.client.get('/delete_ssh_key?ssh_id=1')
        self.assertEqual(302, res.status_code)
        self.assertIn('/ssh_key', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("SSH Key successfully deleted!", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.delete')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_removeresources(self, flash, avatar, delete, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        delete.side_effect = self.delete_response
        self.login(avatar)
        res = self.client.post('/manage_inf/infid/removeresources', data={'vm_list': '1,2'})
        self.assertEqual(302, res.status_code)
        self.assertIn('/infrastructures', res.headers['location'])
        self.assertEqual(flash.call_args_list[0][0], ("VMs 1,2 successfully deleted.", 'success'))

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    @patch("app.infra")
    def test_infrastructure_state(self, infra, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/infrastructures/state?infid=infid')
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'{"state":"configured","vm_states":{"0":"configured"}}\n', res.data)

    @patch("app.utils.getIMUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    def test_owners(self, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/owners/infid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Current Owners:<br><ul><li>user1</li><li>user2</li></ul>', res.data)

    @patch("app.utils.getIMUserAuthData")
    @patch("app.utils.avatar")
    def test_share_token(self, avatar, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        self.login(avatar)
        res = self.client.get('/share_token')
        self.assertEqual(200, res.status_code)
        expected_res = ('<p>Copy your token to share (expires in 500 secs): ' +
                        '<a class="btn btn-outline-success btn-sm" id="copyTokenBtn" ' +
                        'onclick="navigator.clipboard.writeText(\'token\')">' +
                        '<i class="fa fa-copy"></i> Copy</a></p>')
        self.assertEqual(expected_res, res.data.decode('utf-8'))

    def test_oai(self):
        namespace = {'oaipmh': 'http://www.openarchives.org/OAI/2.0/'}

        # Test OAI path
        res = self.client.get('/oai')
        self.assertEqual(200, res.status_code)

        root = etree.fromstring(res.data)

        self.assertEqual(root.find(".//oaipmh:error", namespace).attrib['code'], 'badVerb')

        # Test Identify
        res = self.client.get('/oai?verb=Identify')
        self.assertEqual(200, res.status_code)

        root = etree.fromstring(res.data)

        self.assertEqual(root.find(".//oaipmh:repositoryName", namespace).text, "IM Dashboard")
        self.assertEqual(root.find(".//oaipmh:baseURL", namespace).text, "http://localhost/oai")
        self.assertEqual(root.find(".//oaipmh:protocolVersion", namespace).text, "2.0")
        self.assertIsNotNone(root.find(".//oaipmh:earliestDatestamp", namespace))
        self.assertEqual(root.find(".//oaipmh:deletedRecord", namespace).text, "no")
        self.assertEqual(root.find(".//oaipmh:granularity", namespace).text, "YYYY-MM-DD")
        self.assertEqual(root.find(".//oaipmh:adminEmail", namespace).text, "support@example.com")

        # Test Identify Post with body params
        res = self.client.post('/oai', headers={'Content-Type': 'application/x-www-form-urlencoded'},
                               data="verb=Identify")
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        self.assertEqual(root.find(".//oaipmh:repositoryName", namespace).text, "IM Dashboard")

        # Test GetRecord
        tosca_id = "https://github.com/grycap/tosca/blob/main/templates/simple-node-disk.yml"
        res = self.client.get('/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s' % tosca_id)
        self.assertEqual(200, res.status_code)

        root = etree.fromstring(res.data)

        namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
                      'oaipmh': 'http://www.openarchives.org/OAI/2.0/',
                      'datacite': 'http://datacite.org/schema/kernel-4'}

        self.assertEqual(root.find(".//dc:title", namespaces).text, "Deploy a VM")
        self.assertEqual(root.find(".//dc:creator", namespaces).text, "Miguel Caballer")
        self.assertEqual(root.find(".//dc:date", namespaces).text, "2020-09-08")
        self.assertEqual(root.find(".//oaipmh:identifier", namespaces).text,
                         "https://github.com/grycap/tosca/blob/main/templates/simple-node-disk.yml")
        self.assertEqual(root.find(".//oaipmh:datestamp", namespaces).text,
                         "2020-09-08")
        # self.assertIsNotNone(root.find(".//dc:type", namespace_dc))
        # self.assertIsNotNone(root.find(".//dc:rights", namespace_dc))

        # Test GetRecord with invalid identifier
        tosca_id = 'invalid"id'
        res = self.client.get('/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s' % tosca_id)
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        self.assertEqual(root.find(".//oaipmh:error", namespace).attrib['code'], 'idDoesNotExist')

        # Test ListIdentifiers
        res = self.client.get('/oai?verb=ListIdentifiers&metadataPrefix=oai_dc')
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        elems = root.findall(".//oaipmh:header", namespaces)
        self.assertEqual(len(elems), 1)

        self.assertEqual(root.find(".//oaipmh:identifier", namespaces).text,
                         "https://github.com/grycap/tosca/blob/main/templates/simple-node-disk.yml")

        # Test ListIdentifiers with from
        res = self.client.get('/oai?verb=ListIdentifiers&metadataPrefix=oai_dc&from=2020-09-10')
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        self.assertEqual(root.find(".//oaipmh:error", namespace).attrib['code'], 'noRecordsMatch')

        res = self.client.get('/oai?verb=ListIdentifiers&metadataPrefix=oai_dc&from=2020-09-07')
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        elems = root.findall(".//oaipmh:header", namespaces)
        self.assertEqual(len(elems), 1)

        res = self.client.get('/oai?verb=ListIdentifiers&metadataPrefix=oai_dc&until=2020-09-07')
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        self.assertEqual(root.find(".//oaipmh:error", namespace).attrib['code'], 'noRecordsMatch')

        # Test ListRecords oai_dc
        res = self.client.get('/oai?verb=ListRecords&metadataPrefix=oai_dc')
        self.assertEqual(200, res.status_code)

        root = etree.fromstring(res.data)

        self.assertEqual(root.find(".//dc:title", namespaces).text, "Deploy a VM")
        self.assertEqual(root.find(".//dc:creator", namespaces).text, "Miguel Caballer")
        self.assertEqual(root.find(".//dc:date", namespaces).text, "2020-09-08")
        self.assertEqual(root.find(".//oaipmh:identifier", namespaces).text,
                         "https://github.com/grycap/tosca/blob/main/templates/simple-node-disk.yml")
        self.assertEqual(root.find(".//oaipmh:datestamp", namespaces).text,
                         "2020-09-08")
        # self.assertIsNotNone(root.find(".//dc:type", namespace_dc))
        # self.assertIsNotNone(root.find(".//dc:rights", namespace_dc))

        # Test ListRecords oai_openaire
        res = self.client.get('/oai?verb=ListRecords&metadataPrefix=oai_openaire')
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        elems = root.findall(".//oaipmh:identifier", namespaces)
        self.assertEqual(len(elems), 1)
        self.assertEqual(root.find(".//datacite:creatorName", namespaces).text, "Miguel Caballer")

        res = self.client.get('/oai?verb=ListRecords&metadataPrefix=oai_dc&until=2020-09-07')
        self.assertEqual(200, res.status_code)
        root = etree.fromstring(res.data)
        self.assertEqual(root.find(".//oaipmh:error", namespace).attrib['code'], 'noRecordsMatch')

        # Test ListMetadataFormats
        res = self.client.get('/oai?verb=ListMetadataFormats')
        self.assertEqual(200, res.status_code)

        root = etree.fromstring(res.data)

        prefixes = root.findall(".//oaipmh:metadataPrefix", namespaces)
        prefixes_text = [prefix.text for prefix in prefixes]

        self.assertIn('oai_dc', prefixes_text)
        self.assertIn('oai_openaire', prefixes_text)

        # Test ListSets
        res = self.client.get('/oai?verb=ListSets')
        self.assertEqual(200, res.status_code)

        root = etree.fromstring(res.data)

        self.assertEqual(root.find(".//oaipmh:error", namespace).attrib['code'], 'noSetHierarchy')

    @patch("hvac.Client")
    def test_secret(self, hvac):
        hvac_mock = MagicMock()
        hvac.return_value = hvac_mock
        hvac_mock.read.return_value = {"data": {"data": "some_data\\nmore_data"}}
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer your_token'
        res = self.client.get('/secret/secret_id')
        del self.client.environ_base['HTTP_AUTHORIZATION']
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'some_data\nmore_data', res.data)

    @patch("app.utils.getUserAuthData")
    @patch('requests.get')
    @patch("app.utils.avatar")
    @patch("app.flash")
    def test_reconfigure_with_params(self, flash, avatar, get, user_data):
        user_data.return_value = "type = InfrastructureManager; token = access_token"
        get.side_effect = self.get_response
        self.login(avatar)
        res = self.client.get('/reconfigure/infid')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'<input type="text" class="form-control" id="param1"', res.data)
        self.assertIn(b'<input type="hidden" name="reconfigure_template"', res.data)

    @patch("app.utils.getUserAuthData")
    @patch("app.utils.avatar")
    def test_auth_file(self, avatar, user_data):
        user_data.return_value = ("type = InfrastructureManager; token = access_token\\n" +
                                  "id = test; username = test; password = some\\\\npassword")
        self.login(avatar)
        res = self.client.get('/auth_file')
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'type = InfrastructureManager; token = access_token\n' +
                         b'id = test; username = test; password = some\\npassword', res.data)
