bl_info = {
    "name":"Object Adder",
    "author":"David Cai",
    "version":(1,0),
    "blender":(4,1,1),
    "location":"View 3D > Tool Shelf",
    "warning":"",
    "category":"Materials",
}





import bpy

#*Main Mat Panel
class MatPanel(bpy.types.Panel):
    bl_label = "Shader Library"
    bl_idname = "Mat_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shader_Lib"


    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        column = layout.column()
        column.label(text="Materials")
        column.operator("wood.shader")
        column.operator("glass.shader")
        column.operator("clay.shader")
        
        #Iron Shaders here
        column.label(text="Iron Shaders")
        column.operator("iron.shader")
        column.operator("castiron.shader")
        column.operator("rustyiron.shader")
        column.operator("ranbowiron.shader")

#wood
class Wood(bpy.types.Operator):
    bl_idname = "wood.shader"
    bl_label = "Wood"

    def execute(self, context):
        wood = bpy.data.materials.new(name="Wood")
        wood.use_nodes = True
        
        wood.node_tree.nodes.remove(wood.node_tree.nodes.get('Principled BSDF'))
        
        material_output = wood.node_tree.nodes.get('Material Output')
        material_output.location = (1000, 0)
        
        bsdf = wood.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (600, 0)
        bsdf.inputs[1].default_value = 0.127
        bsdf.inputs[23].default_value = 0.005

        # Color Ramp 1, organe
        color1_node = wood.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-200, 0)
        color1_node.color_ramp.elements[0].position = 0.236
        color1_node.color_ramp.elements[0].color = (0.704, 0.185, 0.018, 1)
        color1_node.color_ramp.elements[1].position = 0.727
        color1_node.color_ramp.elements[1].color = (0.018, 0.003, 0.003, 1)
        
        # Noise
        noise = wood.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-350, 0)
        noise.inputs[2].default_value = 3.6  # Scale
        noise.inputs[3].default_value = 2.7  # Detail
        noise.inputs[4].default_value = 0.592 #roughness
        noise.inputs[5].default_value = 2.3 #lacunar
        noise.inputs[8].default_value = 2 #distortion

        #Voronoi
        voro = wood.node_tree.nodes.new('ShaderNodeTexVoronoi')
        voro.location = (-350, 0)
        voro.inputs[2].default_value = 4.9  # Scale
        voro.inputs[3].default_value = 3.1  # Detail
        voro.inputs[4].default_value = 0.317 #roughness
        voro.inputs[8].default_value = 0.650 #random
        
        #mapping
        mapping = wood.node_tree.nodes.new('ShaderNodeMapping')
        mapping.location = (-500, 0)
        mapping.inputs[3].default_value[0] = 0.5
        mapping.inputs[3].default_value[1] = 1.5

        coord = wood.node_tree.nodes.new('ShaderNodeTexCoord')
        coord.location = (-650, 0)
        
        #upper row link
        wood.node_tree.links.new(coord.outputs[2], mapping.inputs[0])
        wood.node_tree.links.new(mapping.outputs[0], voro.inputs[0])
        wood.node_tree.links.new(voro.outputs[0], noise.inputs[0])
        wood.node_tree.links.new(noise.outputs[1], color1_node.inputs[0])
        wood.node_tree.links.new(color1_node.outputs[0], bsdf.inputs[0])
        
        
        #for bump
        color2_node = wood.node_tree.nodes.new('ShaderNodeValToRGB')
        color2_node.location = (100, -500)
        color2_node.color_ramp.interpolation = 'B_SPLINE'
        color2_node.color_ramp.elements[0].position = 0.632
        color2_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color2_node.color_ramp.elements[1].position = 0.841
        color2_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        #bump
        bump = wood.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (450, -400)
        bump.inputs[0].default_value = 0.592
        
        #link the color ranp
        wood.node_tree.links.new(color1_node.outputs[0], color2_node.inputs[0])
        wood.node_tree.links.new(color2_node.outputs[0], bump.inputs[2])
        wood.node_tree.links.new(bump.outputs[0], bsdf.inputs[5])
        
        
        #color ramp for roughness
        color3_node = wood.node_tree.nodes.new('ShaderNodeValToRGB')
        color3_node.location = (-200, -400)
        color3_node.color_ramp.interpolation = 'B_SPLINE'
        color3_node.color_ramp.elements[0].position = 0.086
        color3_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color3_node.color_ramp.elements[1].position = 0.777
        color3_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        
        noise1 = wood.node_tree.nodes.new('ShaderNodeTexNoise')
        noise1.location = (-350, -400)
        noise1.inputs[3].default_value = 2.5  # Detail
        noise1.inputs[4].default_value = 0.433 #roughness
        noise1.inputs[5].default_value = 2.3 #lacunar

        #to roughness
        wood.node_tree.links.new(noise1.outputs[0], color3_node.inputs[0])
        wood.node_tree.links.new(color3_node.outputs[0], bsdf.inputs[2])
        
        #connect to output
        wood.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = wood
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}
     
#glass   
class Glass(bpy.types.Operator):
    bl_idname = "glass.shader"  
    bl_label = "Glass"

    def execute(self, context):
        cglass = bpy.data.materials.new(name="Glass")
        cglass.use_nodes = True
        
        cglass.node_tree.nodes.remove(cglass.node_tree.nodes.get('Principled BSDF'))
        
        material_output = cglass.node_tree.nodes.get('Material Output')
        material_output.location = (200, 0)
        
        gl = cglass.node_tree.nodes.new('ShaderNodeBsdfGlass')
        gl.location = (0, 0)
        gl.inputs[0].default_value = (0.874, 0.905, 1, 1)
        gl.inputs[2].default_value = 1.450
        
        cglass.node_tree.links.new(gl.outputs[0], material_output.inputs[0])
        
        bpy.context.object.active_material = cglass
       
        bpy.ops.ed.undo_push(message="Update Undo Stack")
       
        return {'FINISHED'}

#clay       
class Clay(bpy.types.Operator):
    bl_idname = "clay.shader"
    bl_label = "Clay"

    def execute(self, context):
        clay = bpy.data.materials.new(name="clay")
        clay.use_nodes = True
        
        clay.node_tree.nodes.remove(clay.node_tree.nodes.get('Principled BSDF'))
        
        material_output = clay.node_tree.nodes.get('Material Output')
        material_output.location = (900, 300)
        
        bsdf = clay.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (580, 300)
        bsdf.inputs[7].default_value = 0.305
        bsdf.inputs[8].default_value[0] = 2.6

        #mix
        color_mix1 = clay.node_tree.nodes.new('ShaderNodeMixRGB')
        color_mix1.location = (400, 350)
        color_mix1.inputs[1].default_value = (0.35, 0.204, 0.302, 1) 
        color_mix1.inputs[2].default_value = (0.736, 0.348, 0.701, 1)  

        # Color Ramp 1,
        color1_node = clay.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (100, 350)
        color1_node.color_ramp.interpolation = 'B_SPLINE'
        color1_node.color_ramp.elements[0].position = 0.205
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 0.891
        color1_node.color_ramp.elements[1].color = (1, 1, 1, 1)

        
        # Noise1
        noise = clay.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-50, 350)
        noise.inputs[2].default_value = 8.2  # Scale
        noise.inputs[3].default_value = 2.7  # Detail
        
        clay.node_tree.links.new(noise.outputs[0], color1_node.inputs[0])
        clay.node_tree.links.new(color1_node.outputs[0], color_mix1.inputs[0])
        clay.node_tree.links.new(color_mix1.outputs[0], bsdf.inputs[0])
        
        #bump
        bump = clay.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (400, -140)
        bump.inputs[0].default_value = 0.063
                
        #color ramp 2
        color2_node = clay.node_tree.nodes.new('ShaderNodeValToRGB')
        color2_node.location = (100, -160)
        color2_node.color_ramp.interpolation = 'B_SPLINE'
        color2_node.color_ramp.elements[0].position = 0.750
        color2_node.color_ramp.elements[0].color = (1, 1, 1, 1)
        color2_node.color_ramp.elements[1].position = 0.914
        color2_node.color_ramp.elements[1].color = (0, 0, 0, 1)

        #noise 2
        noise1 = clay.node_tree.nodes.new('ShaderNodeTexNoise')
        noise1.location = (-50, -160)
        noise1.inputs[2].default_value = 4.1  # scale
        noise1.inputs[3].default_value = 0  # Detail
        noise1.inputs[4].default_value = 0.592  #roughness
        noise1.inputs[5].default_value = 2.3 #lacunar

        #Voronoi
        voro = clay.node_tree.nodes.new('ShaderNodeTexVoronoi')
        voro.location = (-200, -160)
        voro.inputs[2].default_value = 3.9  # Scale
        voro.inputs[3].default_value = 3.1  # Detail
        voro.inputs[4].default_value = 0.317 #roughness
        voro.inputs[8].default_value = 0.650 #random
        

        clay.node_tree.links.new(voro.outputs[0], noise1.inputs[0])
        clay.node_tree.links.new(noise1.outputs[0], color2_node.inputs[0])
        clay.node_tree.links.new(color2_node.outputs[0], bump.inputs[2])
        clay.node_tree.links.new(bump.outputs[0], bsdf.inputs[5])
        
        #connect to output
        clay.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = clay
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")
        
        return {'FINISHED'}

#Iron1
class Iron1(bpy.types.Operator):
    bl_idname = "iron.shader"
    bl_label = "Iron"

    def execute(self, context):
        iron = bpy.data.materials.new(name="Iron")
        iron.use_nodes = True
        
        iron.node_tree.nodes.remove(iron.node_tree.nodes.get('Principled BSDF'))
        
        material_output = iron.node_tree.nodes.get('Material Output')
        material_output.location = (200, 0)
        
        bsdf = iron.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs[1].default_value = 1.0  # metallic
        bsdf.location = (-200, 0)
        
        # Color Ramp 1
        color1_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-600, 150)
        color1_node.color_ramp.elements[0].position = 0
        color1_node.color_ramp.elements[0].color = (0.156, 0.090, 0.074, 1)
        color1_node.color_ramp.elements[1].position = 0.645
        color1_node.color_ramp.elements[1].color = (0.342, 0.309, 0.254, 1)
        
        # Color Ramp 2
        color2_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color2_node.location = (-600, -150)
        color2_node.color_ramp.elements[0].position = 0.127
        color2_node.color_ramp.elements[0].color = (0.01, 0.01, 0.01, 1)
        color2_node.color_ramp.elements[1].position = 0.645
        color2_node.color_ramp.elements[1].color = (0.187, 0.187, 0.187, 1) 
        
        # Noise 
        noise = iron.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-800, 0)
        noise.inputs[2].default_value = 3.0  # Scale
        noise.inputs[3].default_value = 3.4  # Detail
        noise.inputs[5].default_value = 2.2  # Roughness
        noise.inputs[8].default_value = 0.1  # Distortion
        
        iron.node_tree.links.new(noise.outputs[0], color1_node.inputs[0])
        iron.node_tree.links.new(noise.outputs[0], color2_node.inputs[0])
        iron.node_tree.links.new(color1_node.outputs[0], bsdf.inputs[0])
        iron.node_tree.links.new(color2_node.outputs[0], bsdf.inputs[2])
        iron.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])
        
        bpy.context.object.active_material = iron
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")
        
        return {'FINISHED'}

#Iron2
class Iron2Cast(bpy.types.Operator):
    bl_idname = "castiron.shader"
    bl_label = "Cast Iron"

    def execute(self, context):
        iron = bpy.data.materials.new(name="Cast Iron")
        iron.use_nodes = True
        
        iron.node_tree.nodes.remove(iron.node_tree.nodes.get('Principled BSDF'))
        
        material_output = iron.node_tree.nodes.get('Material Output')
        material_output.location = (200, 0)
        
        bsdf = iron.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (-200, 0)
        bsdf.inputs[0].default_value = (0.074, 0.071, 0.08, 1)
        bsdf.inputs[1].default_value = 1.0  # metallic
        
        
        # Color Ramp
        color1_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-600, 150)
        color1_node.color_ramp.elements[0].position = 0.455
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 1
        color1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        #bump
        bump = iron.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (-600, -150)
        bump.inputs[0].default_value = 0.067
        
        # Noise
        noise = iron.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-800, 0)
        noise.inputs[2].default_value = 141.7  # Scale
        noise.inputs[3].default_value = 7.6  # Detail

        #Link
        iron.node_tree.links.new(noise.outputs[0], color1_node.inputs[0])
        iron.node_tree.links.new(noise.outputs[0], bump.inputs[2])
        iron.node_tree.links.new(color1_node.outputs[0], bsdf.inputs[2]) #roughness
        iron.node_tree.links.new(bump.outputs[0], bsdf.inputs[5]) #normal
        iron.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])
        
        bpy.context.object.active_material = iron
        bpy.ops.ed.undo_push(message="Update Undo Stack")
        return {'FINISHED'}

#Iron3
class Iron3Rusty(bpy.types.Operator):
    bl_idname = "rustyiron.shader"
    bl_label = "Rusty Iron"

    def execute(self, context):
        iron = bpy.data.materials.new(name="Rusty Iron")
        iron.use_nodes = True
        
        iron.node_tree.nodes.remove(iron.node_tree.nodes.get('Principled BSDF'))
        
        material_output = iron.node_tree.nodes.get('Material Output')
        material_output.location = (1000, 0)
        
        #mix shader
        mix = iron.node_tree.nodes.new('ShaderNodeMixShader')
        mix.location = (800, 0)
        
        #upper row
        bsdf1 = iron.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf1.location = (500, 300)
        bsdf1.inputs[1].default_value= 1
        bsdf1.inputs[2].default_value= 0.227
        bsdf1.inputs[12].default_value = 0.618
        bsdf1.inputs[23].default_value = 0.455
        bsdf1.inputs[24].default_value = 0.123
        
        # Color Ramp 1
        color1_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-100, 300)
        color1_node.color_ramp.interpolation = 'B_SPLINE'
        color1_node.color_ramp.elements[0].position = 0.205
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 0.891
        color1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        color_mix1 = iron.node_tree.nodes.new('ShaderNodeMixRGB')
        color_mix1.location = (250, 300)
        color_mix1.inputs[1].default_value = (0.579, 0.141, 0.008, 1) 
        color_mix1.inputs[2].default_value = (0.337, 0.058, 0.009, 1)  
        
        # Noise 
        noise = iron.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-300, 300)
        noise.inputs[2].default_value = 8.2  # Scale
        noise.inputs[3].default_value = 2.7  # Detail

        # link upper half
        iron.node_tree.links.new(noise.outputs[0], color1_node.inputs[0])
        iron.node_tree.links.new(color1_node.outputs[0], color_mix1.inputs[0])
        iron.node_tree.links.new(color_mix1.outputs[0], bsdf1.inputs[0])
        iron.node_tree.links.new(bsdf1.outputs[0], mix.inputs[1])

        #lower parts start here
        bsdf2 = iron.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf2.location = (500, -250)
        bsdf2.inputs[1].default_value= 1
        bsdf2.inputs[2].default_value= 0.559
        
        #color ramp for base color
        color2_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color2_node.location = (100, -250)
        color2_node.color_ramp.interpolation = 'B_SPLINE'
        color2_node.color_ramp.elements[0].position = 0.286
        color2_node.color_ramp.elements[0].color = (0.135, 0.135, 0.135, 1)
        color2_node.color_ramp.elements[1].position = 1
        color2_node.color_ramp.elements[1].color = (0.583, 0.583, 0.583, 1)
        
        #bump
        bump = iron.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (200, -600)
        
        #color ramp for fac
        color3_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color3_node.location = (100, -20)
        color3_node.color_ramp.elements[0].position = 0.345
        color3_node.color_ramp.elements[0].color = (1, 1, 1, 1)
        color3_node.color_ramp.elements[1].position = 0.427
        color3_node.color_ramp.elements[1].color = (0, 0, 0, 1)
        
        #gradient
        grad = iron.node_tree.nodes.new('ShaderNodeTexGradient')
        grad.location = (-100, -250)
        grad.gradient_type = 'DIAGONAL'
        
        #color ramp for normal
        color4_node = iron.node_tree.nodes.new('ShaderNodeValToRGB')
        color4_node.location = (-100, -600)
        color4_node.color_ramp.elements[0].position = 0.032
        color4_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color4_node.color_ramp.elements[1].position = 0.391
        color4_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        # Noise 
        noise = iron.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-300, -250)
        noise.inputs[2].default_value = 10.2  # Scale
        noise.inputs[3].default_value = 8.4  # Detail

        #lower part to mix
        iron.node_tree.links.new(noise.outputs[0], color3_node.inputs[0])
        iron.node_tree.links.new(color3_node.outputs[0], mix.inputs[0])
        iron.node_tree.links.new(noise.outputs[0], color4_node.inputs[0])
        iron.node_tree.links.new(color4_node.outputs[0], bump.inputs[2])
        iron.node_tree.links.new(bump.outputs[0], bsdf2.inputs[5])
        iron.node_tree.links.new(grad.outputs[0], color2_node.inputs[0])
        iron.node_tree.links.new(color2_node.outputs[0], bsdf2.inputs[0])
        iron.node_tree.links.new(bsdf2.outputs[0], mix.inputs[2])
        
        #connect to output
        iron.node_tree.links.new(mix.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = iron

        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}

#Ranbow
class IronRainbow(bpy.types.Operator):
    bl_idname = "ranbowiron.shader"
    bl_label = "Iron Rainbow"

    def execute(self, context):
        rb = bpy.data.materials.new(name="Iron Rainbow")
        rb.use_nodes = True

        rb.node_tree.nodes.remove(rb.node_tree.nodes.get('Principled BSDF'))
        
        material_output = rb.node_tree.nodes.get('Material Output')
        material_output.location = (700, 400)
        
        #mix shader
        mix_shad = rb.node_tree.nodes.new('ShaderNodeMixShader')
        mix_shad.location = (550, 400)
        
        # Color Ramp
        color1_node = rb.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-50, 400)
        color1_node.color_ramp.elements[0].position = 0
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 0.686
        color1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        #Layer Weight
        layerw = rb.node_tree.nodes.new('ShaderNodeLayerWeight')
        layerw.location = (-450, 370)
        
        #link top row
        rb.node_tree.links.new(layerw.outputs[1], color1_node.inputs[0])
        rb.node_tree.links.new(color1_node.outputs[0], mix_shad.inputs[0])
        
        #bsdf1
        bsdf1 = rb.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf1.location = (250, 200)
        bsdf1.inputs[1].default_value = 1
        bsdf1.inputs[2].default_value = 0.091
        bsdf1.inputs[3].default_value = 1.45
        
        # color ramp
        color = rb.node_tree.nodes.new('ShaderNodeValToRGB')
        color.location = (-150, 150)
        color.color_ramp.color_mode = 'HSV'
        color.color_ramp.hue_interpolation = 'FAR'
        color.color_ramp.elements[0].position = 0
        color.color_ramp.elements[0].color = (1, 0, 0.341, 1)
        color.color_ramp.elements[1].position = 1
        color.color_ramp.elements[1].color = (1, 0, 0.621, 1)
        
        
        #Layer Weight2
        layerw2 = rb.node_tree.nodes.new('ShaderNodeLayerWeight')
        layerw2.location = (-450, 160)
        
        #bsdf2
        bsdf2 = rb.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf2.location = (250, -150)
        bsdf2.inputs[0].default_value = (0.8, 0.109, 0.019, 1)
        bsdf2.inputs[1].default_value = 1
        bsdf2.inputs[2].default_value = 0.15
        bsdf2.inputs[3].default_value = 1.45
        
        #link bot
        rb.node_tree.links.new(layerw2.outputs[1], color.inputs[0])
        rb.node_tree.links.new(color.outputs[0], bsdf1.inputs[0])
        rb.node_tree.links.new(bsdf1.outputs[0], mix_shad.inputs[1])
        rb.node_tree.links.new(bsdf2.outputs[0], mix_shad.inputs[2])

        #connect to output
        rb.node_tree.links.new(mix_shad.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = rb
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}

#*Abstract Panel
class AbsPanel(bpy.types.Panel):
    bl_label = "Abstracts"
    bl_idname = "Abs_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = 'Shader_Lib'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "Mat_panel"

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        column = layout.column()
        column.operator("gold.shader")
        column.operator("blue.shader")
        column.operator("vomit.shader")
        column.operator("lines.shader")
        column.operator("floor.shader")

class Gold(bpy.types.Operator):
    bl_idname = "gold.shader"
    bl_label = "Gold"

    def execute(self, context):
        abs = bpy.data.materials.new(name="Gold")
        abs.use_nodes = True
        
        abs.node_tree.nodes.remove(abs.node_tree.nodes.get('Principled BSDF'))
        
        material_output = abs.node_tree.nodes.get('Material Output')
        material_output.location = (700, 400)
        
        #mix shader
        mix_shad = abs.node_tree.nodes.new('ShaderNodeMixShader')
        mix_shad.location = (550, 400)
        
        # Color Ramp
        color1_node = abs.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-50, 400)
        color1_node.color_ramp.elements[0].position = 0
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 0.195
        color1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        #Voronoi
        voro = abs.node_tree.nodes.new('ShaderNodeTexVoronoi')
        voro.location = (-250, 400)
        voro.inputs[2].default_value = 27  # Scale
        
        # Noise1
        noise = abs.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-400, 400)
        noise.noise_type = 'MULTIFRACTAL'
        noise.inputs[2].default_value = 3  # Scale
        noise.inputs[3].default_value = 2.5  # Detail
        noise.inputs[4].default_value = 1 #roughness
        noise.inputs[5].default_value = 1 #lacunar
        
        #mapping + coor
        mapping = abs.node_tree.nodes.new('ShaderNodeMapping')
        mapping.location = (-600, 400)
        mapping.inputs[1].default_value[0] = 5
        coord = abs.node_tree.nodes.new('ShaderNodeTexCoord')
        coord.location = (-750, 400)
        
        #link top row
        abs.node_tree.links.new(coord.outputs[0], mapping.inputs[0])
        abs.node_tree.links.new(mapping.outputs[0], noise.inputs[0])
        abs.node_tree.links.new(noise.outputs[0], voro.inputs[0])
        abs.node_tree.links.new(voro.outputs[1], color1_node.inputs[0])
        abs.node_tree.links.new(color1_node.outputs[0], mix_shad.inputs[0])
        
        #bsdf1
        bsdf1 = abs.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf1.location = (250, 200)
        bsdf1.inputs[0].default_value = (1, 0.599, 0.03, 1)
        bsdf1.inputs[1].default_value = 1
        bsdf1.inputs[2].default_value = 0.073
        bsdf1.inputs[3].default_value = 1.45
        bsdf1.inputs[26].default_value = (0.94, 0.81, 0.378, 1)
        bsdf1.inputs[27].default_value = 1
        
        #bump
        bump = abs.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (50,160)
        
        #bsdf2
        bsdf2 = abs.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf2.location = (250, -150)
        bsdf2.inputs[0].default_value = (0.016, 0.016, 0.022, 1)
        bsdf2.inputs[1].default_value = 1
        bsdf2.inputs[2].default_value = 0.336
        bsdf2.inputs[3].default_value = 1.45
        
        #link bot
        abs.node_tree.links.new(color1_node.outputs[0], bump.inputs[2])
        abs.node_tree.links.new(bump.outputs[0], bsdf1.inputs[5])
        abs.node_tree.links.new(bump.outputs[0], bsdf2.inputs[5])
        abs.node_tree.links.new(bsdf1.outputs[0], mix_shad.inputs[1])
        abs.node_tree.links.new(bsdf2.outputs[0], mix_shad.inputs[2])
        
        #connect to output
        abs.node_tree.links.new(mix_shad.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = abs
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}

class Blue(bpy.types.Operator):
    bl_idname = "blue.shader"
    bl_label = "Blue"

    def execute(self, context):
        abs = bpy.data.materials.new(name="Blue")
        abs.use_nodes = True
        
        abs.node_tree.nodes.remove(abs.node_tree.nodes.get('Principled BSDF'))
        
        material_output = abs.node_tree.nodes.get('Material Output')
        material_output.location = (700, 400)
        
        #bsdf
        bsdf = abs.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (400, 400)
        bsdf.inputs[3].default_value = 1.45
        
        # Color Ramp
        color1_node = abs.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (100, 450)
        color1_node.color_ramp.elements[0].position = 0.518
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 1
        color1_node.color_ramp.elements[1].color = (0.3, 0.664, 1, 1)
        
        #Voronoi
        voro = abs.node_tree.nodes.new('ShaderNodeTexVoronoi')
        voro.location = (-200, 400)
        
        # Noise1
        noise = abs.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-400, 400)
        noise.normalize = False
        noise.inputs[3].default_value = 1  # Detail
        noise.inputs[4].default_value = 0.250 #roughness

        #bump
        bump = abs.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (100, 0)

        #link
        abs.node_tree.links.new(noise.outputs[0], voro.inputs[0])
        abs.node_tree.links.new(voro.outputs[1], color1_node.inputs[0])
        abs.node_tree.links.new(voro.outputs[1], bump.inputs[2])
        abs.node_tree.links.new(bump.outputs[0], bsdf.inputs[5])
        abs.node_tree.links.new(color1_node.outputs[0], bsdf.inputs[0])
        
        #connect to output
        abs.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = abs
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}

class Vomit(bpy.types.Operator):
    bl_idname = "vomit.shader"
    bl_label = "Vomit"

    def execute(self, context):
        abs = bpy.data.materials.new(name="Vomit")
        abs.use_nodes = True
        
        abs.node_tree.nodes.remove(abs.node_tree.nodes.get('Principled BSDF'))
        
        material_output = abs.node_tree.nodes.get('Material Output')
        material_output.location = (700, 400)
        
        #bsdf
        bsdf = abs.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (400, 400)
        bsdf.inputs[3].default_value = 1.45
        
        # Color Ramp
        color_node = abs.node_tree.nodes.new('ShaderNodeValToRGB')
        color_node.location = (100, 380)
        color_node.color_ramp.interpolation = 'CONSTANT'
        color_node.color_ramp.elements[0].position = 0.277
        color_node.color_ramp.elements[0].color = (0.947, 0.672, 0.250, 1)
        color_node.color_ramp.elements[1].position = 0.530
        color_node.color_ramp.elements[1].color = (0.745, 0.386, 0.112, 1)
        color_node.color_ramp.elements.new(0.709)
        color_node.color_ramp.elements[2].color = (0.309, 0.031, 0.031, 1)
        
        # Noise1
        noise = abs.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-150, 380)
        noise.inputs[3].default_value = 0  # Detail

        #link
        abs.node_tree.links.new(noise.outputs[0], color_node.inputs[0])
        abs.node_tree.links.new(color_node.outputs[0], bsdf.inputs[0])
        abs.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = abs
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")
        
        return {'FINISHED'}

class Lines(bpy.types.Operator):
    bl_idname = "lines.shader"
    bl_label = "Red Lines"

    def execute(self, context):
        abs = bpy.data.materials.new(name="Lines")
        abs.use_nodes = True
        
        abs.node_tree.nodes.remove(abs.node_tree.nodes.get('Principled BSDF'))
        
        material_output = abs.node_tree.nodes.get('Material Output')
        material_output.location = (700, 400)
        
        #mix shader
        mix_shad = abs.node_tree.nodes.new('ShaderNodeMixShader')
        mix_shad.location = (550, 400)
        
        # Color Ramp
        color1_node = abs.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-50, 400)
        color1_node.color_ramp.elements[0].position = 0
        color1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color1_node.color_ramp.elements[1].position = 0.109
        color1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        #wave
        wave = abs.node_tree.nodes.new('ShaderNodeTexWave')
        wave.location = (-250, 400)
        wave.inputs[2].default_value = 6.5

        #link top row
        abs.node_tree.links.new(wave.outputs[0], color1_node.inputs[0])
        abs.node_tree.links.new(color1_node.outputs[0], mix_shad.inputs[0])
        
        #bsdf1
        bsdf1 = abs.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf1.location = (250, 200)
        bsdf1.inputs[0].default_value = (0.8, 0, 0.00083, 1)
        bsdf1.inputs[2].default_value = 0.895
        bsdf1.inputs[3].default_value = 1.45
        
        #bump
        bump = abs.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (50,160)
        
        #bsdf2
        bsdf2 = abs.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf2.location = (250, -150)
        bsdf2.inputs[0].default_value = (0.016, 0.016, 0.022, 1)
        bsdf2.inputs[2].default_value = 0.145
        bsdf2.inputs[3].default_value = 1.45
        
        #link bot
        abs.node_tree.links.new(color1_node.outputs[0], bump.inputs[2])
        abs.node_tree.links.new(bump.outputs[0], bsdf1.inputs[5])
        abs.node_tree.links.new(bsdf1.outputs[0], mix_shad.inputs[1])
        abs.node_tree.links.new(bsdf2.outputs[0], mix_shad.inputs[2])
        
        #connect to output
        abs.node_tree.links.new(mix_shad.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = abs

        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}

class Floor(bpy.types.Operator):
    bl_idname = "floor.shader"
    bl_label = "Wood Pattern"

    def execute(self, context):
        wood = bpy.data.materials.new(name="wood")
        wood.use_nodes = True
        
        wood.node_tree.nodes.remove(wood.node_tree.nodes.get('Principled BSDF'))
        
        material_output = wood.node_tree.nodes.get('Material Output')
        material_output.location = (1000, 0)
        
        bsdf = wood.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (600, 0)

        # Color Ramp 1, organe
        color1_node = wood.node_tree.nodes.new('ShaderNodeValToRGB')
        color1_node.location = (-200, 0)
        color1_node.color_ramp.elements[0].position = 0.5
        color1_node.color_ramp.elements[0].color = (0.169, 0.064, 0.02, 1)
        color1_node.color_ramp.elements[1].position = 0.505
        color1_node.color_ramp.elements[1].color = (0.011, 0.009, 0.007, 1)
        
        # Noise
        noise = wood.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-350, 0)
        noise.inputs[4].default_value = 0.433 #roughness
        noise.inputs[5].default_value = 2.3 #lacunar
        noise.inputs[8].default_value = 2 #distortion

        #Voronoi
        voro = wood.node_tree.nodes.new('ShaderNodeTexVoronoi')
        voro.location = (-500, 0)
        voro.inputs[2].default_value = 4.9  # Scale
        voro.inputs[3].default_value = 3.1  # Detail
        voro.inputs[4].default_value = 1
        voro.inputs[8].default_value = 0
        
        #upper row link
        wood.node_tree.links.new(voro.outputs[0], noise.inputs[0])
        wood.node_tree.links.new(noise.outputs[1], color1_node.inputs[0])
        wood.node_tree.links.new(color1_node.outputs[0], bsdf.inputs[0])
        wood.node_tree.links.new(color1_node.outputs[0], bsdf.inputs[8])
        
        #for bump
        color2_node = wood.node_tree.nodes.new('ShaderNodeValToRGB')
        color2_node.location = (100, -500)
        color2_node.color_ramp.interpolation = 'B_SPLINE'
        color2_node.color_ramp.elements[0].position = 0.632
        color2_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color2_node.color_ramp.elements[1].position = 0.995
        color2_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        #bump
        bump = wood.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (450, -400)
        bump.inputs[0].default_value = 0.592
        
        #link the color ranp
        wood.node_tree.links.new(color1_node.outputs[0], color2_node.inputs[0])
        wood.node_tree.links.new(color2_node.outputs[0], bump.inputs[2])
        wood.node_tree.links.new(bump.outputs[0], bsdf.inputs[5])
        
        
        #color ramp for roughness
        color3_node = wood.node_tree.nodes.new('ShaderNodeValToRGB')
        color3_node.location = (-200, -400)
        color3_node.color_ramp.interpolation = 'B_SPLINE'
        color3_node.color_ramp.elements[0].position = 0.086
        color3_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        color3_node.color_ramp.elements[1].position = 1
        color3_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        
        noise1 = wood.node_tree.nodes.new('ShaderNodeTexNoise')
        noise1.location = (-350, -400)
        noise1.inputs[3].default_value = 2.5  # Detail
        noise1.inputs[4].default_value = 0.433 #roughness
        noise1.inputs[5].default_value = 2.3 #lacunar

        #to roughness
        wood.node_tree.links.new(noise1.outputs[0], color3_node.inputs[0])
        wood.node_tree.links.new(color3_node.outputs[0], bsdf.inputs[2])
        
        #connect to output
        wood.node_tree.links.new(bsdf.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = wood
        
        bpy.ops.ed.undo_push(message="Update Undo Stack")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MatPanel) #First panel
    bpy.utils.register_class(Iron1)
    bpy.utils.register_class(Iron2Cast)
    bpy.utils.register_class(Iron3Rusty)
    bpy.utils.register_class(IronRainbow)
    bpy.utils.register_class(Wood)
    bpy.utils.register_class(Glass)
    bpy.utils.register_class(Clay)
    bpy.utils.register_class(AbsPanel) #Second panel
    bpy.utils.register_class(Gold)
    bpy.utils.register_class(Blue)
    bpy.utils.register_class(Vomit)
    bpy.utils.register_class(Lines)
    bpy.utils.register_class(Floor)
    
def unregister():
    bpy.utils.unregister_class(MatPanel)
    bpy.utils.unregister_class(Iron1)
    bpy.utils.unregister_class(Iron2Cast)
    bpy.utils.unregister_class(Iron3Rusty)
    bpy.utils.unregister_class(IronRainbow)
    bpy.utils.unregister_class(Wood)
    bpy.utils.unregister_class(Glass)
    bpy.utils.unregister_class(Clay)
    bpy.utils.unregister_class(AbsPanel)
    bpy.utils.unregister_class(Gold)
    bpy.utils.unregister_class(Blue)
    bpy.utils.unregister_class(Vomit)
    bpy.utils.unregister_class(Lines)
    bpy.utils.unregister_class(Floor)
    
if __name__ == "__main__":
    register()