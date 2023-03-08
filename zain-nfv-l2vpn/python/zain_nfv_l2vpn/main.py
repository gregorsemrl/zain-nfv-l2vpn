# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service

# ------------------------
# SERVICE CALLBACK
# ------------------------
class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        device_module = None
        device = root.devices.device[service.device]
        try:
            for m in device.module:
                if(m.name == 'tailf-ned-cisco-ios-xr'):
                    device_module = 'ios-xr'
                    break
                elif(m.name == 'tailf-ned-huawei-vrp'):
                    device_module = 'huawei-vrp'
                    break
                elif(m.name == 'junos-rpc'):
                    device_module = 'junos'
                    break
                else:
                    continue
        except:
            device_module = None
        
        if(device_module != 'ios-xr'):
            raise ValueError(f'Specified device platform is not supported by this service: {service.device} ({device_module})')
        
        vars = ncs.template.Variables()
        template = ncs.template.Template(service)
        template.apply('zain-nfv-l2vpn-template', vars)


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('zain-nfv-l2vpn-servicepoint', ServiceCallbacks)

    def teardown(self):
        self.log.info('Main FINISHED')
