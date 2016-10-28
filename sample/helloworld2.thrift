namespace java com.miui.metok.cdc.thrift.HelloWorldService2

service HelloWorld2 {
    string ping(),
    string say(1:string msg)
}