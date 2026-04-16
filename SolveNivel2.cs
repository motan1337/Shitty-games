// Save as SolveNivel2.cs
// Compile: csc /r:System.dll SolveNivel2.cs  
// Or just use the PowerShell scripts above

using System;
using System.IO;
using System.Reflection;

class Program {
    static void Main() {
        Console.WriteLine("[*] Loading Nivel-2.exe...");
        
        byte[] asmBytes = File.ReadAllBytes("Nivel-2.exe");
        Assembly asm = Assembly.Load(asmBytes);
        
        Console.WriteLine("[+] Loaded. Entry: " + asm.EntryPoint);
        
        // Enumerate all types and their static string fields
        foreach (Type t in asm.GetTypes()) {
            foreach (FieldInfo f in t.GetFields(BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public)) {
                try {
                    object val = f.GetValue(null);
                    if (val is string s && s.Length > 0) {
                        Console.WriteLine($"  String field: '{s}'");
                    }
                    if (val is byte[] b) {
                        Console.WriteLine($"  Byte[] field: len={b.Length} first={BitConverter.ToString(b, 0, Math.Min(16, b.Length))}");
                    }
                } catch { }
            }
        }
        
        // Just run it
        Console.WriteLine("\n[*] Running entry point...");
        try {
            asm.EntryPoint.Invoke(null, new object[] { new string[0] });
        } catch (Exception ex) {
            Console.WriteLine("Error: " + (ex.InnerException ?? ex).Message);
        }
    }
}
