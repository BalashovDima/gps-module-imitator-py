class NMEA():
    def __init__(self) -> None:
        pass

    def generate_gprmc(self, utc_time, lat, lon, speed_knots, course, date, mag_var):
        """Generates a GPRMC string.

        Args:
        utc_time: UTC time in the format HHMMSS.SSS
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        speed_knots: Speed in knots
        course: Course over ground in degrees
        date: Date in the format DDMMYY
        mag_var: Magnetic variation in degrees

        Returns:
        The generated GPRMC string.
        """

        # Convert latitude and longitude to degrees, minutes, seconds
        lat_deg = int(lat)
        lat_min = (lat - lat_deg) * 60
        lon_deg = int(lon)
        lon_min = (lon - lon_deg) * 60

        # Format latitude and longitude as strings
        lat_str = f"{lat_deg:02d}{lat_min:.4f}"
        lon_str = f"{lon_deg:03d}{lon_min:.4f}"

        # Determine latitude and longitude directions
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_dir = 'E' if lon >= 0 else 'W'

        # Calculate checksum
        data = f"$GPRMC,{utc_time},A,{lat_str},{lat_dir},{lon_str},{lon_dir},{speed_knots:.1f},{course:.1f},{date},{mag_var:.1f},A"
        checksum = 0
        for char in data[1:]:
            checksum ^= ord(char)
        checksum = hex(checksum).upper()[2:]

        # Construct the GPRMC string
        gprmc_str = f"{data}*{checksum}\r\n"
        return gprmc_str
    
    def generate_gpvtg(self, timestamp, course_true, course_magnetic, speed_knots):
        """Generates a GPGVT string.

        Args:
            timestamp: Time stamp in the format HHMMSS.SSS
            course_true: Course over ground, true in degrees
            course_magnetic: Course over ground, magnetic in degrees
            speed_knots: Speed in knots

        Returns:
            The generated GPGVT string.
        """

        # Calculate checksum
        data = f"$GPGVT,{timestamp},{course_true:.1f},{course_magnetic:.1f},{speed_knots:.1f}"
        checksum = 0
        for char in data[1:]:
            checksum ^= ord(char)
        checksum = hex(checksum).upper()[2:]

        # Construct the GPGVT string
        gpvtg_str = f"{data}*{checksum}\r\n"
        return gpvtg_str
    
    def generate_gpgga(self, utc_time, lat, lon, fix_quality, num_sats, hdop, altitude, geoidal_sep):
        """Generates a GPGGA string.

        Args:
            utc_time: UTC time in the format HHMMSS.SSS
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            fix_quality: Fix quality (0-1)
            num_sats: Number of satellites
            hdop: Horizontal dilution of precision
            altitude: Altitude in meters
            geoidal_sep: Geoidal separation in meters

        Returns:
            The generated GPGGA string.
        """

        # Convert latitude and longitude to degrees, minutes, seconds
        lat_deg = int(lat)
        lat_min = (lat - lat_deg) * 60
        lon_deg = int(lon)
        lon_min = (lon - lon_deg) * 60

        # Format latitude and longitude as strings
        lat_str = f"{lat_deg:02d}{lat_min:.4f}"
        lon_str = f"{lon_deg:03d}{lon_min:.4f}"

        # Determine latitude and longitude directions
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_dir = 'E' if lon >= 0 else 'W'

        # Calculate checksum
        data = f"$GPGGA,{utc_time},{lat_str},{lat_dir},{lon_str},{lon_dir},{fix_quality},{num_sats},{hdop:.1f},{altitude:.1f},M,{geoidal_sep:.1f},M,,,*"
        checksum = 0
        for char in data[1:]:
            checksum ^= ord(char)
        checksum = hex(checksum).upper()[2:]

        # Construct the GPGGA string
        gpgga_str = f"{data}{checksum}\r\n"
        return gpgga_str
    
    def generate_gpgsa(self, mode, fix_type, prn_list, pdop):
        """Generates a GPGSA string.

        Args:
            mode: Mode (M=manual, A=automatic)
            fix_type: Fix type (1=no fix, 2=2D fix, 3=3D fix)
            prn_list: List of PRN numbers of used satellites (up to 12)
            pdop: Position dilution of precision

        Returns:
            The generated GPGSA string.
        """

        # Ensure PRN list has correct length
        prn_list = prn_list[:12]
        prn_str = ",".join(map(str, prn_list))
        prn_str += "," * (12 - len(prn_list))  # Fill with empty strings if needed

        # Calculate checksum
        data = f"$GPGSA,{mode},{fix_type},{prn_str},{pdop:.1f},,*"
        checksum = 0
        for char in data[1:]:
            checksum ^= ord(char)
        checksum = hex(checksum).upper()[2:]

        # Construct the GPGSA string
        gpgsa_str = f"{data}{checksum}\r\n"
        return gpgsa_str

    def generate_gpgsv(self, total_msgs, msg_num, total_svs, satellite_data):
        """Generates a GPGSV string.

        Args:
            total_msgs: Total number of messages
            msg_num: Message number
            total_svs: Total number of satellites in view
            satellite_data: List of tuples (prn, elevation, azimuth, snr)

        Returns:
            The generated GPGSV string.
        """

        # Ensure satellite data has correct length
        satellite_data = satellite_data[:4]
        satellite_str = ",".join(f"{prn},{elev},{azim},{snr}" for prn, elev, azim, snr in satellite_data)
        satellite_str += "," * (4 - len(satellite_data))  # Fill with empty strings if needed

        # Calculate checksum
        data = f"$GPGSV,{total_msgs},{msg_num},{total_svs},{satellite_str},*"
        checksum = 0
        for char in data[1:]:
            checksum ^= ord(char)
        checksum = hex(checksum).upper()[2:]

        # Construct the GPGSV string
        gpgsv_str = f"{data}{checksum}\r\n"
        return gpgsv_str
    
    def generate_gpgll(self, lat, lon, utc_time, status='A', mode='A'):
        """Generates a GPGLL string.

        Args:
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            utc_time: UTC time in the format HHMMSS.SSS
            status: Status (A=active, V=void), default is 'A'
            mode: Mode indicator (M=manual, A=automatic), default is 'A'

        Returns:
            The generated GPGLL string.
        """

        # Convert latitude and longitude to degrees, minutes, seconds
        lat_deg = int(lat)
        lat_min = (lat - lat_deg) * 60
        lon_deg = int(lon)
        lon_min = (lon - lon_deg) * 60

        # Format latitude and longitude as strings
        lat_str = f"{lat_deg:02d}{lat_min:.4f}"
        lon_str = f"{lon_deg:03d}{lon_min:.4f}"

        # Determine latitude and longitude directions
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_dir = 'E' if lon >= 0 else 'W'

        # Calculate checksum
        data = f"$GPGLL,{lat_str},{lat_dir},{lon_str},{lon_dir},{utc_time},{status},{mode},*"
        checksum = 0
        for char in data[1:]:
            checksum ^= ord(char)
        checksum = hex(checksum).upper()[2:]

        # Construct the GPGLL string
        gpgll_str = f"{data}{checksum}\r\n"
        return gpgll_str

