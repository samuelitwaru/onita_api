def host(request):
    return {'host_address': request.get_host()}