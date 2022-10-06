import defs
import training_set

TS_PATH='.lha_training_set'
training_set.run_training_set(TS_PATH,
defs.dvorak_prog.left_hand+defs.dvorak_prog.left_hand_shift)

