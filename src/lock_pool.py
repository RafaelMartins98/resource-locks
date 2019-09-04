#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

class resource_lock:

    def __init__(self):
        self._locked = False
        self._clientId = None
        self._timeLimit = None
        self._lockedTimes = 0
        self._lockedTime = None


    def lock(self, client_id, time_limit):
        """
            Blocks the resource if this one is not being used or is inactive, or keeps it blocked 
            if is blocked by current user. In this case, it will delay his release time based on
            time_limit received.

            Return True if the resource has been blocked, otherwise False.
        """
        if not self._locked or self._clientId == client_id:
            self._locked = True
            self._clientId = client_id
            self._timeLimit = datetime.now() + timedelta(seconds=time_limit)
            self._lockedTimes += 1
            return True
        return False

    def urelease(self):
        """
            Releases the resource
        """
        if self._locked:
            self._locked = False
            self._clientId = None
            self._timeLimit = None

    def release(self, client_id):
        """
            Releases the resource if this one has been blocked by the current user.
            
            Returns True if has been release otherwise False.
        """
        if client_id == self._clientId:
            self.urelease()
            return True
        return False

    def test(self):
        """
            Returns the current lock status of the current resource
        """
        return self._locked

    def stat(self):
        """
            Returns the number of total blocks 
        """
        return self._lockedTimes

    def disable(self):
        """
            Sets the resource inactive/unavailable
        """
        self._locked = True
        self._clientId = None
        self._timeLimit = None

    def timeLimit(self):
        return self._timeLimit

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
            N - Size based of total resources.
            K - Maximum blocks allow for each reasource, after reaching k, it sets
            the resource unavailable 
            Y - Maximum number of blocked resources at the same time
            T - Time of lock
        """
        self._locks = [resource_lock() for _ in range(N)]
        self._n = N
        self._k = K
        self._y = Y
        self._t = T

    def clear_expired_locks(self):
        """
            Checks if the resources should be released or not.
        """

        for resource in self._locks:
            if resource._locked and resource._clientId != None:
                time = datetime.now()
                if resource.timeLimit() < time:
                    resource.urelease()

    def lock(self, resource_id, client_id, time_limit):
        """
            Locks the resource till the till the time_limit given.
            
            The locks is only available if the resource is active (not blocked 
            or blocked by the current user) and Y has not being exceeded.

            Returns True if the operation goes well otherwise false.
    
        """
        # if self._y > self.stat_y():
        return self._locks[resource_id].lock(client_id, time_limit)
        # return False

    def release(self, resource_id, client_id):
        """
            Releases the given resource.
            
            Returns True in case of success otherwise False.
        """
        if self._locks[resource_id].test():
            return self._locks[resource_id].release(client_id)
        else:
            return False

    def test(self, resource_id):
        """
            Returns True if the resource given is blocked otherwise False
        """
        return self._locks[resource_id].test()

    def test_disabled(self, resource_id):
        """
            Returns True if the resource is blocked otherwise False.
        """
        return self._locks[resource_id].stat() == self._k

    def stat(self, resource_id):
        """
            Returns the number of resource locks based on the given id.
        """
        return self._locks[resource_id].stat()

    def stat_y(self):
        """
            Number of blocked resources at the same time.
        """
        rec = 0
        for resource in self._locks:
            if resource.test():
                rec += 1
        return rec

    def stat_n(self):
        """
            Number of available resources.
        """
        rec = 0
        for resource in self._locks:
            if not resource.test():
                rec += 1
        return rec

    def disable_expired_resources(self):
        for i in range(self._n):
            if self._locks[i].stat() == self._k:
                self._locks[i].disable()

    def __repr__(self):
        """
            Output formatting
        """
        output = ""
        resource_id = 0
        for resource in self._locks:
            if resource._locked and resource._clientId != None:
                output += "resource " + str(resource_id) + " blocked by client with id " + str(resource._clientId) \
                          + " till " + str(resource.timeLimit()) + "\n"
            elif resource._locked:
                output += "resource " + str(resource_id) + " inactive \n"
            else:
                output += "resource " + str(resource_id) + " free \n"
            resource_id += 1

        return output