def get_dead_pos(pos, base, length):
    target_left = base - (length / 2)
    target_right = base + (length / 2)
    if pos < target_left:
        return target_left
    elif pos > target_right:
        return target_right
    else:
        return pos


def pid_move(pos, base, P_co, I_co, D_co, setp_i, max_i, last_dif, time=1):
    dif = base - pos
    setp_p = dif * P_co
    setp_i = setp_i + (dif * I_co) * time
    if setp_i > max_i:
        setp_i = max_i
    elif setp_i < -max_i:
        setp_i = -max_i
    setp_d = (dif - last_dif) * D_co / time
    setp = setp_p + setp_i + setp_d
    return setp, setp_i, dif