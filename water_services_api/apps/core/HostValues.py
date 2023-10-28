class HostValues():
    """docstring for ClassName"""

    def domain(request):
        return request.scheme + '://' + request.META['HTTP_HOST']
