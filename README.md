# lattice
```lattice``` is an application for provisioning network-based cross-connects in a Data Centre environment.

```lattice``` supports either Arista or Juniper devices (QFX, EX (Traditional or ELS), ACX and MX) and provision cross-connects as either VXLAN, L2VPN, VPLS or Q-in-Q depending on hardware capabilities.

Cross-connects *should* also be supported across a homogenous network comprised of the above devices (where the cross-connect type is supported).

###Issues/Branching:

Use the following format for code branches:

* feat: new feature
* doc: documentation-only changes
* bug: fixes bug

Follow with issue number from Github repo, then brief description of purpose eg:

feat/12/add-restful-hooks

Create and checkout from the CLI using:

```git checkout -b feat/12/add-restful-hooks```

