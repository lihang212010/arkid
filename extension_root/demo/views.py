from django.http import HttpResponse


def global_say_helloworld(request):
    return HttpResponse("Hello ArkID from Extensition")


def tenant_say_helloworld(request, tenant_uuid):
    return HttpResponse(f"Hello Tenant {tenant_uuid} from Extensition")
