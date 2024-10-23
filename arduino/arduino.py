import time
import serial
import serial.tools.list_ports
import numpy as np
import pandas as pd

def arduino_connect(port_name=''):
    """ Measures data form an attached Nicla Sense ME and returns measured data as a list.

    Parameters
    ----------
    n_readings : number

    Returns
    -------
    data_table : list
    """

    dev = ''
    ports = serial.tools.list_ports.comports()
    for n in ports:
        print(n)
        if 'Nicla' in n.description:
            dev = n.device

    if len(port_name):
        dev = port_name

    if not len(port_name):
        print("Please input a port name for you Nicla - suggestions above")

    if len(dev):
        return serial.Serial(port=dev, baudrate=115200, timeout=.1)


def arduino_read(column_titles, chip, n_readings=10, r_readings=10):
    """ Measures data form an attached Arduino and returns measured data as a list.

    Parameters
    ----------
    column_titles : list
    chip : PySerial object - defined using the command serial.Serial()
    n_readings : number
    r_readings : number

    Returns
    -------
    data_table : list of lists
    """
    # Clear the buffer for the Nicla serial port
    chip.flush()
    chip.reset_input_buffer()

    # Send number and rate of sensor readings to the Nicla - this will tell the Nicla to start collecting data
    chip.write(bytes("{f0},{f1}".format(f0=n_readings,f1=r_readings), 'utf-8'))

    # Create an numpy array to store the data
    data_table = np.zeros((n_readings, len(column_titles)))
    for n in range(n_readings):
        for readAttempt in range(100):
            data = chip.readline()
            data = np.fromstring(data, sep=',')

            if len(data) == len(column_titles):
                break;
            print("Failed to read data index {} (attempt number {} out of 100). Trying again...".format(n, readAttempt+1))
            time.sleep(0.01)

        # Put the data in the nth row a numpy array
        data_table[n,:] = data

    chip.close()

    return data_table


def arduino_save(data, column_titles):
    """ Saves data from the Nicla to a CSV file.

    Parameters
    ----------
    data : numpy.ndarray - e.g., array([[  0.  ,   0.  ],[  0.  ,   0.  ]])
    column_titles : list

    Returns
    -------
    None
    """
    # Put the data in a DataFrame
    data = pd.DataFrame(data, columns=column_titles)
    data.to_csv('data_' + str(len(data)) + '.csv')

