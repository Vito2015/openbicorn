namespace java com.miui.metok.cdc.thrift.HelloWorldService

service HelloWorld {
    string ping(),
    string say(1:string msg)
}