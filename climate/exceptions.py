# Copyright (c) 2013 Mirantis Inc.
# Copyright (c) 2013 Bull.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from climate.openstack.common.gettextutils import _  # noqa
from climate.openstack.common import log as logging


LOG = logging.getLogger(__name__)


class ClimateException(Exception):
    """Base Climate Exception.

    To correctly use this class, inherit from it and define
    a 'msg_fmt' and 'code' properties.
    """
    msg_fmt = _("An unknown exception occurred")
    code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            self.kwargs['code'] = self.code

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except KeyError:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception(_('Exception in string format operation'))
                for name, value in kwargs.iteritems():
                    LOG.error("%s: %s" % (name, value))

                message = self.msg_fmt

        super(ClimateException, self).__init__(message)


class NotFound(ClimateException):
    """Object not found exception."""
    msg_fmt = _("Object with %(object)s not found")
    code = 404


class NotAuthorized(ClimateException):
    msg_fmt = _("Not authorized")
    code = 403


class PolicyNotAuthorized(NotAuthorized):
    msg_fmt = _("Policy doesn't allow %(action)s to be performed")


class ConfigNotFound(ClimateException):
    msg_fmt = _("Could not find config at %(path)s")
