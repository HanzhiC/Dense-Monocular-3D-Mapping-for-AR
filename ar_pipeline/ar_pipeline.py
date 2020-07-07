import bpy


# switch on nodes and get reference
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

# Clear all nodes in a mat
def clear_material( material ):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()

materials = bpy.data.materials

def create_shadowcatecher(name):
    mat_name = name

    material = materials.new( mat_name )

    if not material:
        material = materials.new( mat_name )

    # We clear it as we'll define it completely
    clear_material( material )

    material.use_nodes = True

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    #Some nodes
    diffuse1 = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
    diffuse2 = nodes.new( type = 'ShaderNodeBsdfDiffuse' )

    transp = nodes.new ( type = 'ShaderNodeBsdfTransparent')

    mix = nodes.new ( type = 'ShaderNodeMixShader')

    rgb2bw = nodes.new(type="ShaderNodeRGBToBW")

    s2rgb = nodes.new(type="ShaderNodeShaderToRGB")

    colorramp = nodes.new(type="ShaderNodeValToRGB")

    output = nodes.new( type = 'ShaderNodeOutputMaterial' )

    # Some setting for nodes

    diffuse2.inputs[0].default_value = (0,0,0,1)


    #With names
    link1 = links.new( diffuse1.outputs['BSDF'], s2rgb.inputs['Shader'] )
    link2 = links.new( s2rgb.outputs['Color'], rgb2bw.inputs['Color'] )
    link3 = links.new( rgb2bw.outputs['Val'], colorramp.inputs['Fac'] )
    link4 = links.new( colorramp.outputs['Color'], mix.inputs['Fac'] )
    link5 = links.new( diffuse2.outputs['BSDF'], mix.inputs[1] )
    link6 = links.new( transp.outputs['BSDF'], mix.inputs[2] )
    link5 = links.new( mix.outputs['Shader'], output.inputs['Surface'] )

    material.blend_method = 'BLEND'
    #Or with indices
    #link = links.new( diffuse.outputs[0], output.inputs[0] )
    
def assign_material(obj, materialname):
    """This function assigns a material to an objects mesh.
 
    :param obj: The object to assign the material to.
    :type obj: bpy.types.Object
    :param materialname: The materials name.
    :type materialname: str
 
    """
    if materialname not in bpy.data.materials:
        if materialname in defs.defaultmaterials:
            materials.createPhobosMaterials()
        else:
            # print("###ERROR: material to be assigned does not exist.")
            log("Material to be assigned does not exist.", "ERROR")
            return None
#    obj.data.materials[0] = bpy.data.materials[materialname]
    obj.data.materials.append(bpy.data.materials[materialname])
#    if bpy.data.materials[materialname].use_transparency:
#        obj.show_transparent = True



def create_compositor(img_path):
    # clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # create nodes

    image_node = tree.nodes.new(type='CompositorNodeImage')

    layer_node = tree.nodes.new(type='CompositorNodeRLayers')

    converter = tree.nodes.new(type="CompositorNodeAlphaOver")

    comp_node = tree.nodes.new('CompositorNodeComposite')   

    image_node.image = bpy.data.images[img_path]
    image_node.location = 0,0
    comp_node.location = 400,0

    # link nodes
    links = tree.links
    link1 = links.new(image_node.outputs[0], converter.inputs[1])
    link2 = links.new(layer_node.outputs[0], converter.inputs[2])
    link3 = links.new(converter.outputs[0], comp_node.inputs[0])

def prepare_camera(focal):
    focal = 21
    scene = bpy.context.collection

    cam_data = bpy.data.cameras.new('camera')
    cam_data.lens = focal
    cam = bpy.data.objects.new('camera', cam_data)
    scene.objects.link(cam)
    bpy.context.scene.camera = cam

    cam.location.x = 0
    cam.location.y = 0
    cam.location.z = 0

    cam.rotation_mode = 'XYZ'
    cam.rotation_euler[0] = 0
    cam.rotation_euler[1] = 3.1416
    cam.rotation_euler[2] = 3.1416
    
def set_sun_light(position, rotation, energy, color=(1,1,1)):
    bpy.ops.object.light_add(type="SUN")
    light_ob = bpy.context.object
    light_ob.location = position
    light_ob.rotation_euler = rotation
    light = light_ob.data
    light.energy = energy
    light.color = color
    
def render(resolution_x, resolution_y, path):
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still = True)


def place_object(location, rotation, path):
    # TODO: set location and rotation of the object we want to place, then it will place the object at that pose.
    pass

def create_catcherplane(location, rotation):
    # TODO: after placing the object, we will need to know the bottom location of that object, so that we can place a plane under
    # it for shadow projection.
    pass 

def import_scene(path):
    # TODO: import 3D scene, I think it might be better to call pcl_visualizer 
    pass
    


set_sun_light((0,-1.211,0),(2.9844,0.6876,2.2165),8)
catcher = bpy.data.objects['Plane']
assign_material(catcher, "shadow_catcher")
create_compositor('city.png')
prepare_camera(21)
path = 'C://Users//Lenovo//Desktop//img.jpg'
render(1241, 376, path)