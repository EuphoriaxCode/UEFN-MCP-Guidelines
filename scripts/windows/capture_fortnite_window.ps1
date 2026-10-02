param([string]$Out = "$env:TEMP\fn_shot.png", [switch]$Front)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W33 {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
[W33]::SetProcessDPIAware() | Out-Null
$p = Get-Process -Name "FortniteClient-Win64-Shipping" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $p) { Write-Output "no window"; exit 1 }
$hwnd = $p.MainWindowHandle
$r = New-Object W33+RECT
[W33]::GetWindowRect($hwnd, [ref]$r) | Out-Null
$w = $r.R - $r.L; $h = $r.B - $r.T
$bmp = New-Object System.Drawing.Bitmap $w, $h
$g = [System.Drawing.Graphics]::FromImage($bmp)
if ($Front) {
  [W33]::ShowWindow($hwnd, 9) | Out-Null
  [W33]::SetForegroundWindow($hwnd) | Out-Null
  Start-Sleep -Milliseconds 700
  $g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
} else {
  $hdc = $g.GetHdc()
  [W33]::PrintWindow($hwnd, $hdc, 2) | Out-Null
  $g.ReleaseHdc($hdc)
}
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output "saved $Out ${w}x${h}"
