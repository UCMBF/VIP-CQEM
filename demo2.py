
import gmsh
import sys

# ==================== DIMENSIONS (mm) ====================
coupling_gap = 0.005      # Q-to-P gap: 5 um

base_length = 2.061658323
base_height = 1.364671296
center_x = 1.026643053
q1_x = 0.192560980
q1_y = 1.115597854
q2_x = 2 * center_x - q1_x

# Cross and its small C-shaped coupling electrode.
qubit_width = 0.014651379
qubit_left_length = 0.159072114
qubit_right_length = 0.127676302
qubit_top_length = 0.159072114
qubit_bottom_length = 0.161165168
qubit_left = q1_x - qubit_left_length
qubit_right = q1_x + qubit_right_length
qubit_top = q1_y + qubit_top_length
qubit_bottom = q1_y - qubit_bottom_length
finger_width = 0.004395414
inner_c_x = qubit_right + 0.021977068
inner_c_tip = inner_c_x + 0.017790960
inner_c_top = q1_y + 0.013604852
inner_c_bottom = q1_y - 0.013604852
pad_gap = coupling_gap
outer_c_left = inner_c_x - finger_width - pad_gap
outer_c_right = inner_c_tip + finger_width + pad_gap
outer_c_top = inner_c_top + finger_width + pad_gap
outer_c_bottom = inner_c_bottom - finger_width - pad_gap
pad_wire_width = 0.005023330

# The central interdigital capacitor. "Pitch" is finger-to-finger spacing.
comb_width = 0.006279162
comb_gap = 0.003139581
comb_pitch = 2 * (comb_width + comb_gap)
comb_left = center_x - 0.132908438
comb_top_y = q1_y + 0.037674974
comb_bar_width = 0.008372217
comb_tip_y = q1_y + 0.010465271
pad_finger_top = q1_y + 0.025116650
central_tooth_left = comb_left + 6 * comb_pitch + 0.004186108
central_tooth_width = 0.025116650
comb_right_start = central_tooth_left + central_tooth_width + comb_gap * 2
comb_right = comb_right_start + 6 * comb_pitch + comb_width
pad1_end = comb_left + 6 * comb_pitch
pad2_start = comb_right_start
lower_wire_width = 0.006279162
lower_middle_y = q1_y - 0.014651379
lower_bottom_y = q1_y - 0.029302758
lower_split_x = comb_left + 0.072211868
lower_split_gap = 0.010465271

# Left resonator: wire width, bend radius and repeated rows.
resonator_width = 0.003558192
bend_radius = 0.019884014
row_spacing = 2 * bend_radius
resonator_left = 0.069070786
resonator_right = 0.351633095
resonator_top_y = 0.759778651
resonator_bottom_y = 0.119304086
resonator_end_x = 0.336981716
fork_left = q1_x - 0.048140245
fork_right = q1_x + 0.043954137
fork_top = qubit_bottom + 0.037674974
fork_bottom = qubit_bottom - 0.016744433
fork_width = 0.012558325

# Ground openings and top control lines.
qubit_ground_gap = 0.016744433
pad_ground_gap = 0.035000000
comb_ground_gap = 0.016744433
control_width = 0.002930276
control_gap = 0.003767497
control_bottom = base_height - 0.064884678


gmsh.initialize()
gmsh.model.add("Liang_chip_metal_only")

metal_base = gmsh.model.occ.addRectangle(
    0, 0, 0,
    base_length, base_height
)

# "openings" will be the cutouts
openings = []

# q1
qubit_parts = []
q1_horizontal = gmsh.model.occ.addRectangle(
    qubit_left, q1_y - qubit_width / 2, 0,
    qubit_left_length + qubit_right_length, qubit_width
)
qubit_parts.append((2, q1_horizontal))

q1_vertical = gmsh.model.occ.addRectangle(
    q1_x - qubit_width / 2, qubit_bottom, 0,
    qubit_width, qubit_top_length + qubit_bottom_length
)
qubit_parts.append((2, q1_vertical))

q1_stem = gmsh.model.occ.addRectangle(
    qubit_right - finger_width / 2, q1_y - finger_width / 2, 0,
    inner_c_x - qubit_right + finger_width, finger_width
)
qubit_parts.append((2, q1_stem))

q1_c_vertical = gmsh.model.occ.addRectangle(
    inner_c_x - finger_width / 2, inner_c_bottom - finger_width / 2, 0,
    finger_width, inner_c_top - inner_c_bottom + finger_width
)
qubit_parts.append((2, q1_c_vertical))

q1_c_top = gmsh.model.occ.addRectangle(
    inner_c_x - finger_width / 2, inner_c_top - finger_width / 2, 0,
    inner_c_tip - inner_c_x + finger_width / 2, finger_width
)
qubit_parts.append((2, q1_c_top))

q1_c_bottom = gmsh.model.occ.addRectangle(
    inner_c_x - finger_width / 2, inner_c_bottom - finger_width / 2, 0,
    inner_c_tip - inner_c_x + finger_width / 2, finger_width
)
qubit_parts.append((2, q1_c_bottom))

Q1, _ = gmsh.model.occ.fuse(qubit_parts[:1], qubit_parts[1:])

# copied q1 and mirror to make q2
Q2 = gmsh.model.occ.copy(Q1)
gmsh.model.occ.mirror(Q2, 1, 0, 0, -center_x)

# p1
pad_parts = []
p1_c_right = gmsh.model.occ.addRectangle(
    outer_c_right - finger_width / 2, outer_c_bottom - finger_width / 2, 0,
    finger_width, outer_c_top - outer_c_bottom + finger_width
)
pad_parts.append((2, p1_c_right))

p1_c_top = gmsh.model.occ.addRectangle(
    outer_c_left - finger_width / 2, outer_c_top - finger_width / 2, 0,
    outer_c_right - outer_c_left + finger_width, finger_width
)
pad_parts.append((2, p1_c_top))

p1_c_bottom = gmsh.model.occ.addRectangle(
    outer_c_left - finger_width / 2, outer_c_bottom - finger_width / 2, 0,
    outer_c_right - outer_c_left + finger_width, finger_width
)
pad_parts.append((2, p1_c_bottom))

p1_top_lip = gmsh.model.occ.addRectangle(
    outer_c_left - finger_width / 2, q1_y + finger_width / 2 + pad_gap, 0,
    finger_width, outer_c_top - q1_y - pad_gap
)
pad_parts.append((2, p1_top_lip))

p1_bottom_lip = gmsh.model.occ.addRectangle(
    outer_c_left - finger_width / 2, outer_c_bottom - finger_width / 2, 0,
    finger_width, q1_y - outer_c_bottom - pad_gap
)
pad_parts.append((2, p1_bottom_lip))

p1_middle_prong = gmsh.model.occ.addRectangle(
    inner_c_x + finger_width / 2 + pad_gap, q1_y - pad_wire_width / 2, 0,
    outer_c_right - inner_c_x - pad_gap, pad_wire_width
)
pad_parts.append((2, p1_middle_prong))

p1_long_wire = gmsh.model.occ.addRectangle(
    outer_c_right, q1_y - pad_wire_width / 2, 0,
    comb_left - outer_c_right + comb_width, pad_wire_width
)
pad_parts.append((2, p1_long_wire))

P1_outer, _ = gmsh.model.occ.fuse(pad_parts[:1], pad_parts[1:])
P2_outer = gmsh.model.occ.copy(P1_outer)
gmsh.model.occ.mirror(P2_outer, 1, 0, 0, -center_x)

# c
coupler_parts = []
coupler_bar = gmsh.model.occ.addRectangle(
    comb_left, comb_top_y, 0,
    comb_right - comb_left, comb_bar_width
)
coupler_parts.append((2, coupler_bar))

for first_x in [comb_left, comb_right_start]:
    for i in range(7):
        finger_x = first_x + i * comb_pitch
        finger = gmsh.model.occ.addRectangle(
            finger_x, comb_tip_y, 0,
            comb_width, comb_top_y + comb_bar_width - comb_tip_y
        )
        coupler_parts.append((2, finger))

coupler_middle_tooth = gmsh.model.occ.addRectangle(
    central_tooth_left, comb_tip_y, 0,
    central_tooth_width, comb_top_y - comb_tip_y + comb_bar_width
)
coupler_parts.append((2, coupler_middle_tooth))

coupler_stem = gmsh.model.occ.addRectangle(
    center_x - comb_width / 2, comb_top_y, 0,
    comb_width, 0.016744433
)
coupler_parts.append((2, coupler_stem))

C, _ = gmsh.model.occ.fuse(coupler_parts[:1], coupler_parts[1:])

# Add the upward fingers and bottom tracks to the connecting pads.
p1_parts = P1_outer.copy()
p2_parts = P2_outer.copy()
for i in range(6):
    p1_finger = gmsh.model.occ.addRectangle(
        comb_left + comb_width + comb_gap + i * comb_pitch,
        q1_y, 0, comb_width, pad_finger_top - q1_y
    )
    p1_parts.append((2, p1_finger))
    p2_finger = gmsh.model.occ.addRectangle(
        comb_right_start + comb_width + comb_gap + i * comb_pitch,
        q1_y, 0, comb_width, pad_finger_top - q1_y
    )
    p2_parts.append((2, p2_finger))

p1_finger_base = gmsh.model.occ.addRectangle(
    comb_left, q1_y - comb_bar_width / 2, 0,
    pad1_end - comb_left, comb_bar_width
)
p1_parts.append((2, p1_finger_base))

p2_finger_base = gmsh.model.occ.addRectangle(
    pad2_start, q1_y - comb_bar_width / 2, 0,
    comb_right - pad2_start, comb_bar_width
)
p2_parts.append((2, p2_finger_base))

p1_lower_vertical = gmsh.model.occ.addRectangle(
    comb_left, lower_bottom_y - lower_wire_width / 2, 0,
    lower_wire_width, q1_y - lower_bottom_y + lower_wire_width
)
p1_parts.append((2, p1_lower_vertical))

p1_lower_middle = gmsh.model.occ.addRectangle(
    comb_left, lower_middle_y - lower_wire_width / 2, 0,
    comb_right - comb_left - lower_wire_width - comb_gap * 3, lower_wire_width
)
p1_parts.append((2, p1_lower_middle))

p1_lower_bottom = gmsh.model.occ.addRectangle(
    comb_left, lower_bottom_y - lower_wire_width / 2, 0,
    lower_split_x - lower_split_gap / 2 - comb_left, lower_wire_width
)
p1_parts.append((2, p1_lower_bottom))

p2_lower_vertical = gmsh.model.occ.addRectangle(
    comb_right - lower_wire_width, lower_bottom_y - lower_wire_width / 2, 0,
    lower_wire_width, q1_y - lower_bottom_y + lower_wire_width
)
p2_parts.append((2, p2_lower_vertical))

p2_lower_bottom = gmsh.model.occ.addRectangle(
    lower_split_x + lower_split_gap / 2, lower_bottom_y - lower_wire_width / 2, 0,
    comb_right - lower_split_x - lower_split_gap / 2, lower_wire_width
)
p2_parts.append((2, p2_lower_bottom))

p2_wire_extension = gmsh.model.occ.addRectangle(
    pad2_start, q1_y - pad_wire_width / 2, 0,
    2 * center_x - outer_c_right - pad2_start, pad_wire_width
)
p2_parts.append((2, p2_wire_extension))

P1, _ = gmsh.model.occ.fuse(p1_parts[:1], p1_parts[1:])
P2, _ = gmsh.model.occ.fuse(p2_parts[:1], p2_parts[1:])

# openings
left_openings = []
q1_horizontal_opening = gmsh.model.occ.addRectangle(
    qubit_left - qubit_ground_gap, q1_y - qubit_width / 2 - qubit_ground_gap, 0,
    qubit_left_length + qubit_right_length + 2 * qubit_ground_gap, qubit_width + 2 * qubit_ground_gap
)
left_openings.append((2, q1_horizontal_opening))

q1_vertical_opening = gmsh.model.occ.addRectangle(
    q1_x - qubit_width / 2 - qubit_ground_gap, qubit_bottom - qubit_ground_gap, 0,
    qubit_width + 2 * qubit_ground_gap, qubit_top_length + qubit_bottom_length + 2 * qubit_ground_gap
)
left_openings.append((2, q1_vertical_opening))

q1_capacitor_opening = gmsh.model.occ.addRectangle(
    outer_c_left - finger_width / 2 - pad_ground_gap / 2, outer_c_bottom - finger_width / 2 - pad_ground_gap, 0,
    outer_c_right - outer_c_left + finger_width + pad_ground_gap, outer_c_top - outer_c_bottom + finger_width + 2 * pad_ground_gap
)
left_openings.append((2, q1_capacitor_opening))

p1_wire_opening = gmsh.model.occ.addRectangle(
    outer_c_right, q1_y - 0.054419408, 0,
    comb_left - outer_c_right + comb_ground_gap, 0.108838815
)
left_openings.append((2, p1_wire_opening))

right_openings = gmsh.model.occ.copy(left_openings)
gmsh.model.occ.mirror(right_openings, 1, 0, 0, -center_x)
openings = openings + left_openings + right_openings

coupler_opening = gmsh.model.occ.addRectangle(
    comb_left - comb_ground_gap, lower_bottom_y - lower_wire_width / 2 - comb_ground_gap * 3, 0,
    comb_right - comb_left + 2 * comb_ground_gap, comb_top_y + comb_bar_width + comb_ground_gap - (lower_bottom_y - lower_wire_width / 2 - comb_ground_gap * 3)
)
openings.append((2, coupler_opening))


track_width = resonator_width
u_width = fork_width

parts = []
left_x = resonator_left
right_x = resonator_right
entry_x = q1_x

# Thirteen straight horizontal rows, joined by twelve semicircles.
for row in range(13):
    row_y = resonator_top_y - row * row_spacing
    row_end = right_x - bend_radius
    if row == 0:
        row_end = entry_x - bend_radius
    straight = gmsh.model.occ.addRectangle(
        left_x + bend_radius, row_y - track_width / 2, 0,
        row_end - left_x - bend_radius, track_width
    )
    parts.append((2, straight))

for turn in range(12):
    bend_y = resonator_top_y - (turn + 0.5) * row_spacing
    bend_x = left_x + bend_radius
    if turn % 2 == 1:
        bend_x = right_x - bend_radius

    outer_radius = bend_radius + track_width / 2
    inner_radius = bend_radius - track_width / 2
    outer_disk = gmsh.model.occ.addDisk(bend_x, bend_y, 0, outer_radius, outer_radius)
    inner_disk = gmsh.model.occ.addDisk(bend_x, bend_y, 0, inner_radius, inner_radius)
    ring, _ = gmsh.model.occ.cut([(2, outer_disk)], [(2, inner_disk)])

    cutter_x = bend_x
    if turn % 2 == 1:
        cutter_x = bend_x - 2 * outer_radius
    half_cutter = gmsh.model.occ.addRectangle(
        cutter_x, bend_y - 2 * outer_radius, 0,
        2 * outer_radius, 4 * outer_radius
    )
    half_ring, _ = gmsh.model.occ.cut(ring, [(2, half_cutter)])
    parts = parts + half_ring

last_row_y = resonator_top_y - 12 * row_spacing
bend_centers = [
    (entry_x - bend_radius, resonator_top_y + bend_radius),
    (left_x + bend_radius, last_row_y - bend_radius),
    (left_x + bend_radius, resonator_bottom_y + bend_radius)
]
for bend_number in range(3):
    bend_x, bend_y = bend_centers[bend_number]
    outer_radius = bend_radius + track_width / 2
    inner_radius = bend_radius - track_width / 2
    outer_disk = gmsh.model.occ.addDisk(bend_x, bend_y, 0, outer_radius, outer_radius)
    inner_disk = gmsh.model.occ.addDisk(bend_x, bend_y, 0, inner_radius, inner_radius)
    ring, _ = gmsh.model.occ.cut([(2, outer_disk)], [(2, inner_disk)])

    cutter_x = bend_x
    cutter_y = bend_y
    if bend_number == 0:
        cutter_x = bend_x - 2 * outer_radius
    if bend_number == 1:
        cutter_y = bend_y - 2 * outer_radius
    side_cutter = gmsh.model.occ.addRectangle(
        cutter_x, bend_y - 2 * outer_radius, 0,
        2 * outer_radius, 4 * outer_radius
    )
    top_bottom_cutter = gmsh.model.occ.addRectangle(
        bend_x - 2 * outer_radius, cutter_y, 0,
        4 * outer_radius, 2 * outer_radius
    )
    quarter_ring, _ = gmsh.model.occ.cut(ring, [(2, side_cutter), (2, top_bottom_cutter)])
    parts = parts + quarter_ring

entry = gmsh.model.occ.addRectangle(
    entry_x - track_width / 2, resonator_top_y + bend_radius, 0,
    track_width, fork_bottom - resonator_top_y - bend_radius
)
lower_vertical = gmsh.model.occ.addRectangle(
    left_x - track_width / 2, resonator_bottom_y + bend_radius, 0,
    track_width, last_row_y - bend_radius - resonator_bottom_y - bend_radius
)
bottom_wire = gmsh.model.occ.addRectangle(
    left_x + bend_radius, resonator_bottom_y - track_width / 2, 0,
    resonator_end_x - left_x - bend_radius, track_width
)
parts = parts + [(2, entry), (2, lower_vertical), (2, bottom_wire)]

# u thing between the resonator and qubit
fork_base = gmsh.model.occ.addRectangle(
    fork_left - u_width / 2, fork_bottom - u_width / 2, 0,
    fork_right - fork_left + u_width, u_width
)
fork_left_arm = gmsh.model.occ.addRectangle(
    fork_left - u_width / 2, fork_bottom - u_width / 2, 0,
    u_width, fork_top - fork_bottom + u_width / 2
)
fork_right_arm = gmsh.model.occ.addRectangle(
    fork_right - u_width / 2, fork_bottom - u_width / 2, 0,
    u_width, fork_top - fork_bottom + u_width / 2
)
parts = parts + [(2, fork_base), (2, fork_left_arm), (2, fork_right_arm)]
R1, _ = gmsh.model.occ.fuse(parts[:1], parts[1:])


control_lines = []
for control_x in [q1_x, q2_x]:
    line = gmsh.model.occ.addRectangle(
        control_x - control_width / 2, control_bottom, 0,
        control_width, base_height - control_bottom
    )
    control_lines.append((2, line))
    opening = gmsh.model.occ.addRectangle(
        control_x - control_width / 2 - control_gap, control_bottom - control_gap, 0,
        control_width + 2 * control_gap, base_height - control_bottom + control_gap
    )
    openings.append((2, opening))

c_control_top = gmsh.model.occ.addRectangle(
    center_x - 0.002093054, base_height - 0.079536057, 0,
    0.004186108, 0.079536057
)

c_control_stem = gmsh.model.occ.addRectangle(
    center_x - 0.001046527, base_height - 0.180002656, 0,
    0.002093054, 0.102559653
)

C_control, _ = gmsh.model.occ.fuse([(2, c_control_top)], [(2, c_control_stem)])

c_control_opening = gmsh.model.occ.addRectangle(
    center_x - 0.002093054 - control_gap, base_height - 0.180002656 - control_gap, 0,
    0.004186108 + 2 * control_gap, 0.180002656 + control_gap
)
openings.append((2, c_control_opening))


all_openings, _ = gmsh.model.occ.fuse(openings[:1], openings[1:])

ground, _ = gmsh.model.occ.cut([(2, metal_base)], all_openings)

gmsh.model.occ.fragment(R1, ground)

gmsh.model.occ.synchronize()

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

