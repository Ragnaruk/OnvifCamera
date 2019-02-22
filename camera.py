from onvif import ONVIFCamera
from time import sleep
import credentials


class Camera:
    def __init__(self):
        self.my_cam = ONVIFCamera(
            credentials.ip,
            credentials.port,
            credentials.login,
            credentials.password
        )

        print('Device information: ' + str(self.my_cam.devicemgmt.GetDeviceInformation()))
        print('--------------------------------------------------------------------------------')

        # Getting hostname
        print('Device hostname: ' + str(self.my_cam.devicemgmt.GetHostname().Name))
        print('--------------------------------------------------------------------------------')

        # Getting system date and time
        dt = self.my_cam.devicemgmt.GetSystemDateAndTime()
        tz = dt.TimeZone
        year = dt.UTCDateTime.Date.Year
        hour = dt.UTCDateTime.Time.Hour

        print('Timezone: ' + str(tz))
        print('Year: ' + str(year))
        print('Hour: ' + str(hour))
        print('--------------------------------------------------------------------------------')

        # Creating media service
        self.media_service = self.my_cam.create_media_service()

        # Edited "site-packages/zeep/xsd/types/simple.py"
        #     def pythonvalue(self, xmlvalue):
        #         return xmlvalue

        # Getting profiles
        self.profiles = self.media_service.GetProfiles()
        self.media_profile = self.profiles[0]

        print("Profiles: " + str(self.profiles))
        print('--------------------------------------------------------------------------------')

        # Getting token
        token = self.media_profile.token

        print("Token: " + str(token))
        print('--------------------------------------------------------------------------------')

        # Creating PTZ service
        self.ptz = self.my_cam.create_ptz_service()

        # Getting available PTZ services
        request = self.ptz.create_type('GetServiceCapabilities')
        service_capabilities = self.ptz.GetServiceCapabilities(request)

        print("Service capabilities: " + str(service_capabilities))
        print('--------------------------------------------------------------------------------')

        # Getting PTZ status
        status = self.ptz.GetStatus({'ProfileToken': token})

        print("PTZ status: " + str(status))
        print('--------------------------------------------------------------------------------')
        print('Pan position:' + str(status.Position.PanTilt.x))
        print('Tilt position:' + str(status.Position.PanTilt.y))
        print('Zoom position:' + str(status.Position.Zoom.x))
        print('Pan/Tilt Moving?:' + str(status.MoveStatus.PanTilt))
        print('--------------------------------------------------------------------------------')

        # Getting PTZ configuration options for getting option ranges
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media_profile.PTZConfiguration.token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)

        print('PTZ configuration options: ' + str(ptz_configuration_options))
        print('--------------------------------------------------------------------------------')

        # Getting move options
        self.request_continuous_move = self.ptz.create_type('ContinuousMove')
        self.request_continuous_move.ProfileToken = self.media_profile.token

        print('Continuous move options: ' + str(self.request_continuous_move))
        print('--------------------------------------------------------------------------------')

        self.request_absolute_move = self.ptz.create_type('AbsoluteMove')
        self.request_absolute_move.ProfileToken = self.media_profile.token

        print('Absolute move options: ' + str(self.request_absolute_move))
        print('--------------------------------------------------------------------------------')

        self.request_relative_move = self.ptz.create_type('RelativeMove')
        self.request_relative_move.ProfileToken = self.media_profile.token

        print('Relative move options: ' + str(self.request_relative_move))
        print('--------------------------------------------------------------------------------')

        self.request_stop = self.ptz.create_type('Stop')
        self.request_stop.ProfileToken = self.media_profile.token

        print('Stop options: ' + str(self.request_stop))
        print('--------------------------------------------------------------------------------')

        # self.request_set_preset = self.ptz.create_type('SetPreset')
        # self.request_set_preset.ProfileToken = self.profiles[0].token
        #
        # self.request_goto_preset = self.ptz.create_type('GoToPreset')
        # self.request_goto_preset.ProfileToken = self.profiles[0].token

        self.stop()

    # Stop any movement
    def stop(self):
        self.request_stop.PanTilt = True
        self.request_stop.Zoom = True

        self.ptz.Stop(self.request_stop)

        # print('Stopping camera')

    # Continuous move functions
    def perform_move(self, timeout):
        # Start continuous move
        ret = self.ptz.ContinuousMove(self.request_continuous_move)

        # Wait a certain time
        sleep(timeout)

        # Stop continuous move
        self.stop()

        # print('Continuous move completed')
        sleep(2)

    def move_tilt(self, velocity, timeout):
        print('Tilting with velocity: \'' + str(velocity) + '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.PanTilt.x = 0.0
        status.Position.PanTilt.y = velocity

        self.request_continuous_move.Velocity = status.Position

        self.perform_move(timeout)

    def move_pan(self, velocity, timeout):
        print('Panning with velocity: \'' + str(velocity) + '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.PanTilt.x = velocity
        status.Position.PanTilt.y = 0.0

        self.request_continuous_move.Velocity = status.Position

        self.perform_move(timeout)

    def move_zoom(self, velocity, timeout):
        print('Zooming with velocity: \'' + str(velocity) + '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.Zoom.x = velocity

        self.request_continuous_move.Velocity = status.Position

        self.perform_move(timeout)
