# -*- coding: utf-8 -*-

from simmate.calculators.vasp.tasks.base import VaspTask
from simmate.calculators.vasp.inputs.potcar_mappings import PBE_ELEMENT_MAPPINGS_LOW_QUALITY


class MITRelaxationTask(VaspTask):

    # This uses the PBE functional with POTCARs that have lower electron counts
    # and convergence criteria.
    functional = "PBE"
    potcar_mappings=PBE_ELEMENT_MAPPINGS_LOW_QUALITY
    
    # These are all input settings for this task. Note a lot of settings
    # depend on the structure/composition being analyzed.
    incar = dict(
        
        # These settings are the same for all structures regardless of composition
        ALGO="Fast",
        EDIFF=1.0e-05,
        ENCUT=520,
        IBRION=2,
        ICHARG=1,
        ISIF=3,
        ISMEAR=-5,
        ISPIN=2,
        ISYM=0,
        LORBIT=11,
        LREAL="Auto",
        LWAVE=False,
        NELM=200,
        NELMIN=6,
        NSW=99,
        PREC="Accurate",
        SIGMA=0.05,
        KSPACING=0.4,  # !!! This is where we are different from pymatgen right now
        
        # The magnetic moments are dependent on what the composition and oxidation
        # states are. These are relevent because we have ISPIN=2
        MAGMOM__smart_magmom={
            "default": 0.6,
            "Ce": 5,
            "Ce3+": 1,
            "Co": 0.6,
            "Co3+": 0.6,
            "Co4+": 1,
            "Cr": 5,
            "Dy3+": 5,
            "Er3+": 3,
            "Eu": 10,
            "Eu2+": 7,
            "Eu3+": 6,
            "Fe": 5,
            "Gd3+": 7,
            "Ho3+": 4,
            "La3+": 0.6,
            "Lu3+": 0.6,
            "Mn": 5,
            "Mn3+": 4,
            "Mn4+": 3,
            "Mo": 5,
            "Nd3+": 3,
            "Ni": 5,
            "Pm3+": 4,
            "Pr3+": 2,
            "Sm3+": 5,
            "Tb3+": 6,
            "Tm3+": 2,
            "V": 5,
            "W": 5,
            "Yb3+": 1,
            },
        
        # We run LDA+U for certain compositions. This is a complex configuration
        # so be sure to read the "__smart_ldau" modifier for more information.
        multiple_keywords__smart_ldau=dict(
            LDAU__auto=True,
            LDAUTYPE=2,
            LDAUPRINT=1,
            LMAXMIX__auto=True,
            LDAUJ={},
            # The way you read these below... {F: {Ag: 2}} means if the structure
            # is a fluoride, then we set the MAGMOM for Ag to 2. Any element that
            # isn't listed defaults to 0.
            LDAUL={
                "F":{
                    "Ag":2,
                    "Co":2,
                    "Cr":2,
                    "Cu":2,
                    "Fe":2,
                    "Mn":2,
                    "Mo":2,
                    "Nb":2,
                    "Ni":2,
                    "Re":2,
                    "Ta":2,
                    "V":2,
                    "W":2,
                    },
                "O":{
                    "Ag":2,
                    "Co":2,
                    "Cr":2,
                    "Cu":2,
                    "Fe":2,
                    "Mn":2,
                    "Mo":2,
                    "Nb":2,
                    "Ni":2,
                    "Re":2,
                    "Ta":2,
                    "V":2,
                    "W":2,
                    },
                "S":{
                    "Fe":2,
                    "Mn":2.5,
                },
            },
            LDAUU={
                "F":{
                    "Ag":1.5,
                    "Co":3.4,
                    "Cr":3.5,
                    "Cu":4,
                    "Fe":4.0,
                    "Mn":3.9,
                    "Mo":4.38,
                    "Nb":1.5,
                    "Ni":6,
                    "Re":2,
                    "Ta":2,
                    "V":3.1,
                    "W":4.0,
                    },
                "O":{
                    "Ag":1.5,
                    "Co":3.4,
                    "Cr":3.5,
                    "Cu":4,
                    "Fe":4.0,
                    "Mn":3.9,
                    "Mo":4.38,
                    "Nb":1.5,
                    "Ni":6,
                    "Re":2,
                    "Ta":2,
                    "V":3.1,
                    "W":4.0,
                    },
                "S":{
                    "Fe":1.9,
                    "Mn":2.5,
                    },
                }
            ),
        )
