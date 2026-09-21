import gmsh
import sys

# #initialize gmsh
gmsh.initialize()
gmsh.model.add("Chip_Layout")


#base
base_length = 1.88664
base_height = 1.2446

#q1 padding
q1_padding_width = 0.04555
q1_padding_length = 0.27349
q1_horizontal_margin = 0.01607
q1_vertical_margin = 0.070

q1_x = q1_horizontal_margin + (q1_padding_length/2)
q1_y = base_height - q1_vertical_margin - (q1_padding_length/2)
q1_width = 0.01587
q1_arm_length = 0.26029

#coupler padding
coupler_line_width = 0.005
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


#padding geometries
metal_base = gmsh.model.occ.addRectangle(
    0,
    0,
    0,
    base_length,
    base_height
)

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

#final padding geometries
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

#wiring geometries

#q1 wiring
q1_wiring_horizontal = gmsh.model.occ.addRectangle(
    q1_x - (q1_arm_length/2),
    q1_y - (q1_width/2),
    0,
    q1_arm_length,
    q1_width
)

q1_wiring_vertical = gmsh.model.occ.addRectangle(
    q1_x - (q1_width/2),
    q1_y - (q1_arm_length/2),
    0,
    q1_width,
    q1_arm_length
)

q1_wiring_fused = gmsh.model.occ.fuse(
    [(2, q1_wiring_horizontal)],
    [(2, q1_wiring_vertical)]
)

#coupler wiring
coupler_wiring_width = 0.0044
coupler_stem_length = 0.01741
coupler_horizontal_length = 0.02
coupler_gap = 0.005
coupler_vertical_length = 0.02914

coupler_wiring_stem = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2),
    q1_y - (coupler_wiring_width/2),
    0,
    coupler_stem_length,
    coupler_wiring_width
)

coupler_wiring_bridge = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length,
    q1_y - (coupler_vertical_length/2),
    0,
    coupler_wiring_width,
    coupler_vertical_length
)

coupler_wiring_top = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length,
    q1_y + (coupler_vertical_length/2) - coupler_wiring_width,
    0,
    coupler_horizontal_length,
    coupler_wiring_width
)

coupler_wiring_bottom = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length,
    q1_y - (coupler_vertical_length/2),
    0,
    coupler_horizontal_length,
    coupler_wiring_width
)

coupler_fused = gmsh.model.occ.fuse(
    [(2, coupler_wiring_stem)],
    [(2, coupler_wiring_bridge),
     (2, coupler_wiring_top),
     (2, coupler_wiring_bottom)]
)

#second coupler part
coupler_2_middle_width = 0.01
coupler_2_middle_length = 0.016
coupler_2_bridge_length = 0.048
coupler_2_wiring_width = 0.004
coupler_2_horizontal_length = 0.03930
coupler_2_vertical_length = 0.01638

coupler_wiring_middle2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + coupler_wiring_width + coupler_gap,
    q1_y - (coupler_2_middle_width/2),
    0,
    coupler_2_middle_length,
    coupler_2_middle_width
)

coupler_wiring_bridge2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + coupler_wiring_width + coupler_gap + coupler_2_middle_length,
    q1_y - (coupler_2_bridge_length/2),
    0,
    coupler_2_wiring_width,
    coupler_2_bridge_length
)

coupler_wiring_bottom2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + coupler_wiring_width + coupler_gap + coupler_2_middle_length + coupler_2_wiring_width - coupler_2_horizontal_length,
    q1_y - (coupler_2_bridge_length/2),
    0,
    coupler_2_horizontal_length,
    coupler_2_wiring_width
)

coupler_wiring_top2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + coupler_wiring_width + coupler_gap + coupler_2_middle_length + coupler_2_wiring_width - coupler_2_horizontal_length,
    q1_y + (coupler_2_bridge_length/2) - coupler_2_wiring_width,
    0,
    coupler_2_horizontal_length,
    coupler_2_wiring_width
)

coupler_wiring_vertical_bottom2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + coupler_wiring_width + coupler_gap + coupler_2_middle_length + coupler_2_wiring_width - coupler_2_horizontal_length,
    q1_y - (coupler_2_bridge_length/2),
    0,
    coupler_2_wiring_width,
    coupler_2_vertical_length
)

coupler_wiring_vertical_top2 = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + coupler_wiring_width + coupler_gap + coupler_2_middle_length + coupler_2_wiring_width - coupler_2_horizontal_length,
    q1_y + (coupler_2_bridge_length/2) - coupler_2_vertical_length,
    0,
    coupler_2_wiring_width,
    coupler_2_vertical_length
)

coupler2_fused = gmsh.model.occ.fuse(
    [(2, coupler_wiring_middle2)],
    [(2, coupler_wiring_bridge2),
     (2, coupler_wiring_top2),
     (2, coupler_wiring_bottom2),
     (2, coupler_wiring_vertical_bottom2),
     (2, coupler_wiring_vertical_top2)]
)

#p1 wiring
p1_wiring_width = 0.008
p1_wiring_length = 0.46292

p1_wire = gmsh.model.occ.addRectangle(
    q1_x + (q1_arm_length/2) + coupler_stem_length + (coupler_wiring_width * 2) + coupler_gap + coupler_2_middle_length,
    q1_y - (p1_wiring_width/2),
    0,
    p1_wiring_length,
    p1_wiring_width
)

gmsh.model.occ.synchronize()


#gmsh.model.mesh.generate(2)


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

# #finalize
gmsh.finalize()