# -*- coding:utf-8 -*-
#
# hotspot-login-manager
# https://github.com/syam44/Hotspot-Login-Manager
#
# Distributed under the GNU General Public License version 3
# https://www.gnu.org/copyleft/gpl.html
#
# Authors: syam (aks92@free.fr)
#
# Description: Notifications dispatching.
#


#-----------------------------------------------------------------------------
import threading


#-----------------------------------------------------------------------------
class Dispatcher(object):
    ''' Notifications dispatching class (producer).
    '''
    #-----------------------------------------------------------------------------
    def __init__(self):
        self.__lock = threading.Lock()
        self.__observers = set()

    #-----------------------------------------------------------------------------
    def addObserver(self, observer):
        ''' Add an observer, from now on it will receive all broadcast messages.
        '''
        with self.__lock:
            self.__observers.add(observer)


    #-----------------------------------------------------------------------------
    def removeObserver(self, observer):
        ''' Remove an observer, from now on it won't receive any broadcast message.
        '''
        with self.__lock:
            self.__observers.remove(observer)


    #-----------------------------------------------------------------------------
    def notify(self, message):
        ''' Broadcast a message to all listening observers.
        '''
        with self.__lock:
            for observer in self.__observers:
                observer.notify(message)


#-----------------------------------------------------------------------------
class Observer(object):
    ''' Notifications observer class (consumer).
    '''
    #-----------------------------------------------------------------------------
    def __init__(self):
        self.__condition = threading.Condition()
        self.__messages = []


    #-----------------------------------------------------------------------------
    def notify(self, message):
        ''' Add a message to the observer's internal queue.
            It should only be called by the Dispatcher class.
        '''
        self.__condition.acquire()
        self.__messages.append(message)
        self.__condition.notify()
        self.__condition.release()


    #-----------------------------------------------------------------------------
    def getMessages(self, timeout = None):
        ''' Get (and empty) the observer's internal messages queue.
        '''
        self.__condition.acquire()
        if self.__messages == []:
            self.__condition.wait(timeout)
        messages = self.__messages
        self.__messages = []
        self.__condition.release()
        return messages


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
