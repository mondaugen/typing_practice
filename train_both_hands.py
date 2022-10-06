import defs
import training_set

TS_PATH='.bh_training_set'
training_set.run_training_set(TS_PATH,
defs.dvorak_prog.left_hand+defs.dvorak_prog.left_hand_shift+
defs.dvorak_prog.right_hand+defs.dvorak_prog.right_hand_shift)


