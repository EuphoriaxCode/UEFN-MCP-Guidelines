# Materials & textures

## UI material setup
```json
{"materialDomain": "MD_UI", "blendMode": "BLEND_Translucent", "shadingModel": "MSM_Unlit"}
```
Output RGB → `MP_EmissiveColor`, alpha → `MP_Opacity`. `recompile` raises if the shader fails.

## Graph building from the sandbox
`scripts/sandbox/mcp_matlib.py` = tiny DSL (`G('M_Name')`, `g.add/mul/sin/...`, `g.tex(param, texture, uv)`, `g.finish(rgb, a)`).
- Constants: Multiply has `constA/constB` but the lib just makes `Constant` nodes (`r` property).
- Pin names: binary nodes `A`/`B`, Power `Base`/`Exp`, Lerp `A`/`B`/`Alpha`, single-input nodes use `''`,
  Rotator `Coordinate`/`Time` (props `centerX/centerY/speed`), TextureSampleParameter2D in `UVs`, outs `RGB`,`A`,`R`...
- ComponentMask props `r,g,b,a` (bool). Vector param default `{'r','g','b','a'}`.
- **Custom (HLSL) expression**: listed and compiles, but UEFN doesn't support it (missing from the editor palette; risk at publish). Avoid.
- Material params show up in the Assets digest as `@editable var` on a material class.

## Textures
- Import: `TextureTools.import_file(folder_path, asset_name, source_file)` — **fails if the asset exists**.
  To update: import `Name_v2`, repoint (`brush.resourceObject` on Images, `set_texture_parameter` on MIs),
  `get_referencers` on the old one → delete when empty.
- Settings after import: `{"lODGroup":"TEXTUREGROUP_UI","mipGenSettings":"TMGS_NoMipmaps","compressionSettings":"TC_EditorIcon","neverStream":true,"addressX":"TA_Clamp","addressY":"TA_Clamp"}` (`TA_Wrap` for tiling).
- Unicode in paths (é) is fine for import.

## Making the art
- Pillow + numpy SDF renderer in `scripts/art/drawkit.py` (supersampled, antialiased): rounded rects, circles, polygons,
  segments, stars; `chunky()` = Roblox style (hard drop shadow, thick dark outline, vertical gradient, inner bottom shade, gloss).
- **Clip gloss/highlights to the shape** (`cov(d + inset)`), otherwise they poke outside the outline on big shapes.
- Rotate text together with its background (draw upright, then rotate the image), never rotate only the shape.
- Bake all static text (Arial Black + thick stroke looks very Roblox). Generate a 1920×1080 mockup first (`mock_layout.py`).
