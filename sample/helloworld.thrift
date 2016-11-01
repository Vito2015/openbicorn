namespace py HelloWorldService
# namespace java com.miui.metok.bicorn.services.HelloWorldService

service HelloWorld {
    string ping(),
    string say(1:string msg)
}