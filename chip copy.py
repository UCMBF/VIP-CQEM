import gmsh
import sys

# #initialize gmsh
gmsh.initialize()
gmsh.model.add("Chip_Layout")

#base
base_length = 1.88664
base_height = 1.2446

#qubit 1
q1_padding_width = 0.04555
q1_padding_length = 0.27349
q1_horizontal_margin = 0.01607
q1_vertical_margin = 0.070

q1_x = q1_horizontal_margin + (q1_padding_length/2)
q1_y = base_height - q1_vertical_margin - (q1_padding_length/2)
q1_width = 0.01441
q1_arm_length = 0.15131

#coupler
coupler_stem_width = 0.005
coupler_gap = 0.005
coupler_stem_length = 0.01908

coupler_padding_length = 0.08776
coupler_padding_height = 0.135

p1_padding_height = 0.098
p1_padding_length = 0.424

#c
c_padding_height1 = 0.104
c_padding_height2 = 0.02633

c_padding_length1 = 0.27349
c_padding_length2 = 0.24424

#base
metal_base = gmsh.model.occ.addRectangle(
    0,
    0,
    0,
    base_length,
    base_height
)

#q1 padding
q1_padding_horizontal = gmsh.model.occ.addRectangle(
    q1_horizontal_margin,
    base_height - (q1_vertical_margin + (q1_padding_length/2) + (q1_padding_width/2)),  
    0,
    q1_padding_length,
    q1_padding_width
)

q1_padding_vertical = gmsh.model.occ.addRectangle(
    q1_horizontal_margin + (q1_padding_length/2) - (q1_padding_width/2),
    base_height - q1_vertical_margin - q1_padding_length,
    0,
    q1_padding_width,
    q1_padding_length
)

c_padding1 = gmsh.model.occ.addRectangle(
    q1_x + (q1_padding_length/2) + coupler_padding_length + p1_padding_length,
    q1_y - (p1_padding_height/2),
    0,
    c_padding_length1,
    c_padding_height1
)

c_padding2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_padding_length/2) + coupler_padding_length + p1_padding_length + (c_padding_length1/2) - (c_padding_length2/2),
    q1_y - (p1_padding_height/2) - c_padding_height2,
    0,
    c_padding_length2,
    c_padding_height2
)

#final shapes
q1_padding_fused, _ = gmsh.model.occ.fuse(
    [(2, q1_padding_horizontal)],
    [(2, q1_padding_vertical)]
)

coupler_padding = gmsh.model.occ.addRectangle(
    q1_x + (q1_padding_length/2),
    q1_y - (coupler_padding_height/2),
    0,
    coupler_padding_length,
    coupler_padding_height
)

p1_padding = gmsh.model.occ.addRectangle(
    q1_x + (q1_padding_length/2) + coupler_padding_length,
    q1_y - (p1_padding_height/2),
    0,
    p1_padding_length,
    p1_padding_height
)

c_fused, _ = gmsh.model.occ.fuse(
    [(2, c_padding1)],
    [(2, c_padding2)]
)

#mirror
center_x = q1_x + (q1_padding_length/2) + coupler_padding_length + p1_padding_length + (c_padding_length1/2)
copy_of_left_side = gmsh.model.occ.copy(
    [(2, q1_padding_fused[0][0]),
     (2, coupler_padding),
     (2, p1_padding),]
)

gmsh.model.occ.mirror(
    copy_of_left_side,
    1,
    0,
    0,
    -center_x
)

gmsh.model.occ.synchronize()


#gmsh.model.mesh.generate(2)


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

# #finalize
gmsh.finalize()
