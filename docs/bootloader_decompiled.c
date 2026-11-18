/* ===== thunk_FUN_08001338 @ 0800020c | callers: FUN_08002660 ===== */

void thunk_FUN_08001338(void)

{
  (*DAT_08000210)();
  return;
}



/* ===== FUN_08000218 @ 08000218 | callers: FUN_08001072,FUN_080012f4 ===== */

void FUN_08000218(undefined4 *param_1)

{
  bool bVar1;
  
  FUN_0800256a();
  disableIRQinterrupts();
  InstructionSynchronizationBarrier(0xf);
  *DAT_080002a8 = 0xfffcffff;
  *DAT_080002ac = 0xfffcffff;
  *DAT_080002b0 = 0xffffffbf;
  *DAT_080002b4 = 0xffffffbf;
  *DAT_080002b8 = (int)param_1;
  bVar1 = (bool)isCurrentModePrivileged();
  if (bVar1) {
    setMainStackPointer(*param_1);
  }
  enableIRQinterrupts();
                    /* WARNING: Could not recover jumptable at 0x08000250. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)param_1[1])();
  return;
}



/* ===== FUN_080002cc @ 080002cc | callers: thunk_FUN_080002cc ===== */

bool FUN_080002cc(uint param_1,undefined4 param_2)

{
  uint uVar1;
  
  uVar1 = *DAT_08000324;
  if (param_1 < uVar1) {
    (**(code **)(DAT_08000328 + param_1 * 4))(param_2);
  }
  return param_1 < uVar1;
}



/* ===== FUN_08000350 @ 08000350 | callers: FUN_0800039c ===== */

void FUN_08000350(void)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  bool bVar5;
  bool bVar6;
  
  piVar1 = DAT_08000750;
  uVar4 = 0;
  iVar3 = *DAT_08000750;
  do {
    iVar2 = 0x17;
    do {
      bVar5 = iVar2 != 0;
      iVar2 = iVar2 + -1;
    } while (bVar5);
    uVar4 = uVar4 + 1;
    bVar5 = uVar4 == 20000;
    if (uVar4 < 0x4e21) {
      bVar5 = (*(uint *)(iVar3 + 0x10) & 0x80000000) == 0;
    }
    bVar6 = uVar4 < 0x4e21;
  } while (bVar5);
  *(uint *)(iVar3 + 0x10) = *(uint *)(iVar3 + 0x10) | 1;
  uVar4 = 0;
  do {
    bVar5 = (*(uint *)(*piVar1 + 0x10) & 1) != 0;
    if (bVar5) {
      uVar4 = uVar4 + 1;
      bVar6 = uVar4 < 0x4e21;
    }
  } while (bVar6 && (bVar5 && uVar4 != 20000));
  iVar3 = 0x4f;
  do {
    bVar5 = iVar3 != 0;
    iVar3 = iVar3 + -1;
  } while (bVar5);
  return;
}



/* ===== FUN_0800039c @ 0800039c | callers: FUN_08000d04 ===== */

void FUN_0800039c(void)

{
  int *piVar1;
  int iVar2;
  bool bVar3;
  
  FUN_08000350();
  piVar1 = DAT_08000750;
  *(uint *)(*DAT_08000750 + 0xc) = *(uint *)(*DAT_08000750 + 0xc) | 0x40;
  FUN_08000350();
  *(undefined4 *)(*piVar1 + 0x38) = 0x90000;
  iVar2 = DAT_08000754;
  do {
    bVar3 = iVar2 != 0;
    iVar2 = iVar2 + -1;
  } while (bVar3);
  iVar2 = *piVar1;
  *(uint *)(iVar2 + 0xc) = *(uint *)(iVar2 + 0xc) | 0x300;
  iVar2 = DAT_08000758;
  do {
    bVar3 = iVar2 != 0;
    iVar2 = iVar2 + -1;
  } while (bVar3);
  return;
}



/* ===== FUN_080003d6 @ 080003d6 | callers: FUN_08000862,FUN_08000446 ===== */

void FUN_080003d6(uint param_1)

{
  int *piVar1;
  int iVar2;
  uint uVar3;
  bool bVar4;
  undefined1 in_CY;
  
  piVar1 = DAT_08000750;
  uVar3 = 0;
  *(uint *)(*DAT_08000750 + 0x10) = (param_1 & 0x1f) << 6 | 0x20;
  do {
    bVar4 = (*(uint *)(*piVar1 + 0x10) & 0x20) != 0;
    if (bVar4) {
      uVar3 = uVar3 + 1;
      in_CY = uVar3 < 0x4e21;
    }
  } while ((bool)in_CY && (bVar4 && uVar3 != 20000));
  iVar2 = 0x17;
  do {
    bVar4 = iVar2 != 0;
    iVar2 = iVar2 + -1;
  } while (bVar4);
  return;
}



/* ===== FUN_08000402 @ 08000402 | callers: FUN_08000862,FUN_08000446 ===== */

void FUN_08000402(void)

{
  int *piVar1;
  uint uVar2;
  int iVar3;
  bool bVar4;
  undefined1 in_CY;
  
  piVar1 = DAT_08000750;
  uVar2 = 0;
  *(uint *)(*DAT_08000750 + 0x10) = *(uint *)(*DAT_08000750 + 0x10) | 0x10;
  do {
    bVar4 = (*(uint *)(*piVar1 + 0x10) & 0x10) != 0;
    if (bVar4) {
      uVar2 = uVar2 + 1;
      in_CY = uVar2 < 0x4e21;
    }
  } while ((bool)in_CY && (bVar4 && uVar2 != 20000));
  iVar3 = 0x17;
  do {
    bVar4 = iVar3 != 0;
    iVar3 = iVar3 + -1;
  } while (bVar4);
  return;
}



/* ===== FUN_0800042e @ 0800042e | callers: FUN_08000954,FUN_080009e6,FUN_08000c2c,FUN_08000d04,FUN_08000446 ===== */

void FUN_0800042e(undefined1 param_1)

{
  int iVar1;
  
  iVar1 = DAT_08000750;
  *(undefined1 *)(DAT_08000750 + 0xab) = param_1;
  if (*(code **)(iVar1 + 4) == (code *)0x0) {
    return;
  }
                    /* WARNING: Could not recover jumptable at 0x0800043c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(iVar1 + 4))();
  return;
}



/* ===== FUN_0800043e @ 0800043e | callers: FUN_0800179c,FUN_08001408,FUN_08001828,FUN_080014b4,FUN_0800145a,FUN_08001740 ===== */

undefined1 FUN_0800043e(void)

{
  return *(undefined1 *)(DAT_08000750 + 0xab);
}



/* ===== FUN_08000446 @ 08000446 | callers: FUN_08000c2c ===== */

void FUN_08000446(void)

{
  undefined1 uVar1;
  int *piVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  
  piVar2 = DAT_08000750;
  *(uint *)(*DAT_08000750 + 0x24) = (*(uint *)(*DAT_08000750 + 0x24) & 0xffff0000) + 0xa0;
  uVar6 = 0;
  uVar4 = 0x2000a0;
  *(undefined4 *)(*piVar2 + 0x28) = 0x2000a0;
  uVar3 = 0;
  do {
    uVar4 = uVar4 & 0xffff0000 | uVar4 + 0x20 & 0xffff;
    *(uint *)(*piVar2 + uVar3 * 4 + 0x104) = uVar4;
    uVar3 = uVar3 + 1;
  } while (uVar3 < 3);
  FUN_080003d6(0x10);
  FUN_08000402();
  *(uint *)(*piVar2 + 0x800) = *(uint *)(*piVar2 + 0x800) & 0xfffff80f;
  uVar3 = 0;
  do {
    iVar5 = uVar3 * 0x20 + 0x900;
    uVar4 = uVar6;
    if ((*(uint *)(*piVar2 + iVar5) & 0x80000000) != 0) {
      uVar4 = 0x48000000;
    }
    *(uint *)(*piVar2 + iVar5) = uVar4 & 0xfc3fffff | (uVar3 & 0xf) << 0x16;
    *(uint *)(*piVar2 + uVar3 * 0x20 + 0x910) = uVar6;
    *(undefined4 *)(*piVar2 + uVar3 * 0x20 + 0x908) = 0xffffffff;
    iVar5 = uVar3 * 0x20 + 0xb00;
    uVar4 = uVar6;
    if ((*(uint *)(*piVar2 + iVar5) & 0x80000000) != 0) {
      uVar4 = 0x48000000;
    }
    *(uint *)(*piVar2 + iVar5) = uVar4;
    *(uint *)(*piVar2 + uVar3 * 0x20 + 0xb10) = uVar6;
    *(undefined4 *)(*piVar2 + uVar3 * 0x20 + 0xb08) = 0xffffffff;
    uVar4 = uVar3 + 1;
    uVar1 = (undefined1)uVar6;
    *(undefined1 *)(piVar2 + uVar3 * 8 + 0xd) = uVar1;
    *(undefined1 *)(piVar2 + uVar3 * 8 + 0x11) = uVar1;
    uVar3 = uVar4;
  } while (uVar4 < 4);
  iVar5 = *piVar2;
  *(uint *)(iVar5 + 0xb10) = *(uint *)(iVar5 + 0xb10) | 0x60000000;
  *(uint *)(iVar5 + 0xb00) = *(uint *)(iVar5 + 0xb00) | 0x80000000;
  *(undefined1 *)(piVar2 + 0x2a) = uVar1;
  *(undefined1 *)((int)piVar2 + 0xa9) = uVar1;
  *(undefined1 *)((int)piVar2 + 0xaa) = uVar1;
  FUN_0800042e(2);
  return;
}



/* ===== FUN_0800055e @ 0800055e | callers: FUN_08000862,FUN_08000c2c ===== */

void FUN_0800055e(undefined4 param_1,undefined4 param_2,uint param_3,undefined4 param_4)

{
  uint *puVar1;
  uint uVar2;
  uint *puVar3;
  uint uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined1 uVar7;
  undefined4 *puVar8;
  uint *puVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  bool bVar13;
  undefined4 local_28;
  
  puVar1 = DAT_08000750;
  if ((*(uint *)(*DAT_08000750 + 0x14) & 0x10) != 0) {
    uVar2 = *(uint *)(*DAT_08000750 + 0x20);
    uVar4 = uVar2 & 0xf;
    switch((uVar2 << 0xb) >> 0x1c) {
    case 2:
      uVar2 = (uVar2 << 0x11) >> 0x15;
      param_3 = uVar2;
      if ((char)DAT_08000750[uVar4 * 8 + 0x11] != '\x01') {
        param_3 = 0;
      }
      DAT_08000750[uVar4 * 8 + 0x10] = DAT_08000750[uVar4 * 8 + 0x10] + param_3;
      if (puVar1[uVar4 * 8 + 0xf] < param_3) {
        param_3 = puVar1[uVar4 * 8 + 0xf];
      }
      uVar10 = uVar2 + 3 >> 2;
      uVar2 = 0;
      puVar6 = (undefined4 *)puVar1[uVar4 * 8 + 0xe];
      if (uVar10 != 0) {
        do {
          puVar8 = puVar6;
          if (uVar2 < param_3 + 3 >> 2) {
            puVar8 = puVar6 + 1;
            *puVar6 = *(undefined4 *)(*puVar1 + 0x1000);
          }
          uVar2 = uVar2 + 1;
          puVar6 = puVar8;
        } while (uVar2 < uVar10);
      }
      puVar1[uVar4 * 8 + 0xe] = puVar1[uVar4 * 8 + 0xe] + param_3;
      puVar1[uVar4 * 8 + 0xf] = puVar1[uVar4 * 8 + 0xf] - param_3;
      break;
    case 6:
      uVar10 = ((uVar2 << 0x11) >> 0x15) + 3 >> 2;
      uVar2 = 0;
      puVar9 = DAT_08000750 + 6;
      if (uVar10 != 0) {
        do {
          puVar3 = puVar9 + 1;
          *puVar9 = *(uint *)(*puVar1 + 0x1000);
          param_3 = *puVar1 + 0x1000;
          do {
            uVar2 = uVar2 + 1;
            if (uVar10 <= uVar2) goto LAB_0800062e;
            puVar9 = puVar3;
          } while (1 < uVar2);
        } while( true );
      }
LAB_0800062e:
      puVar1[uVar4 * 8 + 0xe] = DAT_0800075c;
    }
    *(uint *)(*puVar1 + 0x14) = *(uint *)(*puVar1 + 0x14) | 0x10;
  }
  uVar2 = 0;
  local_28 = param_4;
  do {
    uVar7 = (undefined1)param_3;
    puVar9 = puVar1 + uVar2 * 8 + 10;
    if ((*(uint *)(*puVar1 + uVar2 * 0x20 + 0xb00) & 0x8000) != 0) {
      iVar5 = uVar2 * 0x20 + 0xb08;
      uVar4 = *(uint *)(*puVar1 + iVar5);
      if (uVar4 != 0) {
        if ((uVar2 == 0) && ((uVar4 & 0x48) != 0)) {
          uVar7 = 1;
          *(undefined1 *)(puVar1 + 0x2a) = 1;
        }
        bVar13 = (uVar4 & 1) != 0;
        if (bVar13) {
          uVar7 = 2;
        }
        if (bVar13) {
          *(undefined1 *)(puVar1 + uVar2 * 8 + 0x11) = uVar7;
        }
        param_3 = *puVar1;
        *(uint *)(param_3 + iVar5) = uVar4;
      }
    }
    uVar4 = *puVar1;
    if ((*(uint *)(uVar4 + uVar2 * 0x20 + 0x900) & 0x8000) != 0) {
      iVar5 = uVar2 * 0x20 + 0x908;
      uVar10 = *(uint *)(uVar4 + iVar5);
      if (uVar10 != 0) {
        if ((((uVar10 & 0x80) != 0) && (uVar4 = (uint)(byte)puVar1[uVar2 * 8 + 0xd], uVar4 == 1)) &&
           (uVar4 = puVar1[uVar2 * 8 + 0xc], uVar4 != 0)) {
          puVar3 = (uint *)FUN_080026c8(uVar2 & 0xff | 0x80);
          local_28 = *DAT_08000760;
          if ((uVar2 & 0x7f) == 0) {
            uVar4 = (uint)*(byte *)((int)&local_28 + (*puVar3 & 3));
          }
          else {
            uVar4 = *puVar3 & 0x7ff;
          }
          uVar12 = puVar1[uVar2 * 8 + 0xc];
          if (uVar4 < puVar1[uVar2 * 8 + 0xc]) {
            uVar12 = uVar4;
          }
          param_3 = uVar12 + 3;
          if (param_3 >> 2 <= (*(uint *)(*puVar1 + uVar2 * 0x20 + 0x918) & 0xffff)) {
            puVar6 = (undefined4 *)*puVar9;
            uVar11 = puVar1[uVar2 * 8 + 0xb];
            puVar8 = (undefined4 *)(*puVar1 + (uVar2 & 0xff) * 0x1000 + 0x1000);
            param_3 = param_3 >> 2;
            uVar4 = 0;
            if (param_3 != 0) {
              do {
                if (uVar4 < uVar11 + 3 >> 2) {
                  *puVar8 = *puVar6;
                }
                else {
                  *puVar8 = 0;
                }
                uVar4 = uVar4 + 1;
                puVar6 = puVar6 + 1;
              } while (uVar4 < param_3);
            }
            *puVar9 = *puVar9 + uVar12;
            puVar1[uVar2 * 8 + 0xc] = puVar1[uVar2 * 8 + 0xc] - uVar12;
            if (uVar12 < puVar1[uVar2 * 8 + 0xb]) {
              uVar4 = puVar1[uVar2 * 8 + 0xb] - uVar12;
            }
            else {
              uVar4 = 0;
            }
            puVar1[uVar2 * 8 + 0xb] = uVar4;
          }
        }
        uVar7 = (undefined1)uVar4;
        bVar13 = (uVar10 & 1) != 0;
        if (bVar13) {
          uVar7 = 2;
        }
        if (bVar13) {
          *(undefined1 *)(puVar1 + uVar2 * 8 + 0xd) = uVar7;
        }
        *(uint *)(*puVar1 + iVar5) = uVar10;
      }
    }
    uVar2 = uVar2 + 1;
  } while (uVar2 < 4);
  return;
}



/* ===== FUN_0800078e @ 0800078e | callers: FUN_08001828,FUN_080009e6,FUN_080014b4 ===== */

void FUN_0800078e(uint param_1,int param_2,uint param_3,int param_4)

{
  int *piVar1;
  int iVar2;
  uint *puVar3;
  uint *puVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  int local_28;
  
  piVar1 = DAT_08000bb4;
  iVar2 = *DAT_08000bb4;
  uVar8 = param_1 & 0x7f;
  if ((param_1 & 0x80) == 0) {
    iVar6 = param_1 * 0x20 + 0xb10;
  }
  else {
    iVar6 = uVar8 * 0x20 + 0x910;
  }
  local_28 = param_4;
  puVar3 = (uint *)FUN_080026c8(param_1);
  puVar4 = (uint *)FUN_080026c8(param_1);
  local_28 = *DAT_08000bb8;
  if ((param_1 & 0x7f) == 0) {
    uVar5 = (uint)*(byte *)((int)&local_28 + (*puVar4 & 3));
  }
  else {
    uVar5 = *puVar4 & 0x7ff;
  }
  if (param_3 == 0) {
    uVar7 = 1;
  }
  else {
    uVar7 = ((param_3 + uVar5) - 1) / uVar5;
  }
  if ((*puVar3 & 0x8000) != 0) {
    if ((param_1 & 0x80) == 0) {
      param_3 = uVar5 * uVar7;
      piVar1[uVar8 * 8 + 0xe] = param_2;
      piVar1[uVar8 * 8 + 0xf] = param_4;
      piVar1[uVar8 * 8 + 0x10] = 0;
      *(undefined1 *)(piVar1 + uVar8 * 8 + 0x11) = 1;
    }
    else {
      piVar1[uVar8 * 8 + 10] = param_2;
      piVar1[uVar8 * 8 + 0xb] = param_4;
      piVar1[uVar8 * 8 + 0xc] = param_3;
      *(undefined1 *)(piVar1 + uVar8 * 8 + 0xd) = 1;
    }
    uVar5 = *(uint *)(iVar2 + iVar6);
    uVar8 = *puVar3;
    if ((param_1 & 0x7f) == 0) {
      uVar5 = uVar5 & 0xfff7ff80 | param_3 & 0x7f | (uVar7 & 1) << 0x13;
    }
    else {
      uVar5 = uVar5 & 0xe0000000 | param_3 & 0x7ffff | (uVar7 & 0x3ff) << 0x13;
    }
    *(uint *)(iVar2 + iVar6) = uVar5;
    *puVar3 = uVar8 | 0x84000000;
    return;
  }
  return;
}



/* ===== FUN_08000862 @ 08000862 | callers: FUN_080018a6,FUN_080009e6,FUN_080014b4 ===== */

void FUN_08000862(uint param_1)

{
  int *piVar1;
  uint *puVar2;
  uint *puVar3;
  int iVar4;
  uint uVar5;
  
  puVar2 = (uint *)FUN_080026c8();
  piVar1 = DAT_08000bb4;
  if ((param_1 & 0x80) == 0) {
    if ((*puVar2 & 0x80000000) != 0) {
      iVar4 = *DAT_08000bb4;
      if ((*(uint *)(iVar4 + 0x14) & 0x80) == 0) {
        *(uint *)(iVar4 + 0x804) = *(uint *)(iVar4 + 0x804) | 0x200;
        uVar5 = *(uint *)(iVar4 + 0x14);
        while ((uVar5 & 0x80) == 0) {
          FUN_0800055e();
          uVar5 = *(uint *)(*piVar1 + 0x14);
        }
      }
      *puVar2 = *puVar2 | 0x40000000;
      *puVar2 = *puVar2 | 0x8000000;
      do {
      } while ((*(uint *)(iVar4 + (param_1 & 0x7f) * 0x20 + 0xb08) & 2) == 0);
      FUN_08000402();
      *(uint *)(*piVar1 + 0x804) = *(uint *)(*piVar1 + 0x804) | 0x400;
    }
    *(undefined1 *)(piVar1 + (param_1 & 0x7f) * 8 + 0x11) = 0;
    return;
  }
  if ((*puVar2 & 0x80000000) != 0) {
    puVar3 = (uint *)(*DAT_08000bb4 + (param_1 & 0x7f) * 0x20 + 0x908);
    *puVar2 = *puVar2 | 0x8000000;
    do {
    } while ((*puVar3 & 0x40) == 0);
    *puVar2 = *puVar2 | 0x40000000;
    do {
    } while ((*puVar3 & 2) == 0);
    FUN_080003d6((*puVar2 << 6) >> 0x1c);
  }
  *(undefined1 *)(piVar1 + (param_1 & 0x7f) * 8 + 0xd) = 0;
  return;
}



/* ===== FUN_0800093c @ 0800093c | callers: FUN_080014b4 ===== */

undefined1 FUN_0800093c(uint param_1)

{
  undefined1 uVar1;
  int iVar2;
  
  iVar2 = DAT_08000bb4 + (param_1 & 0x7f) * 0x20;
  if ((param_1 & 0x80) == 0) {
    uVar1 = *(undefined1 *)(iVar2 + 0x44);
  }
  else {
    uVar1 = *(undefined1 *)(iVar2 + 0x34);
  }
  return uVar1;
}



/* ===== FUN_08000954 @ 08000954 | callers: FUN_080009e6 ===== */

void FUN_08000954(int param_1)

{
  int iVar1;
  uint *puVar2;
  undefined4 uVar3;
  uint uVar4;
  
  if (param_1 == 0) {
    uVar4 = 0;
    do {
      puVar2 = (uint *)FUN_080026c8(uVar4 & 0xff);
      *puVar2 = *puVar2 & 0xffff7fff;
      uVar4 = uVar4 + 1;
    } while (uVar4 < 4);
    uVar3 = 2;
  }
  else {
    puVar2 = (uint *)FUN_080026c8(0x81);
    if ((*puVar2 & 0x8000) == 0) {
      *puVar2 = *puVar2 & 0xfc33f800 | 0x104c8040;
    }
    puVar2 = (uint *)FUN_080026c8(2);
    if ((*puVar2 & 0x8000) == 0) {
      *puVar2 = *puVar2 & 0xfc33f800 | 0x108c8040;
    }
    uVar3 = 4;
  }
  FUN_0800042e(uVar3);
  iVar1 = DAT_08000bb4;
  *(char *)(DAT_08000bb4 + 0xa9) = (char)param_1;
  *(undefined1 *)(iVar1 + 0xaa) = 0;
  return;
}



/* ===== FUN_080009e6 @ 080009e6 | callers: FUN_08000c2c ===== */

void FUN_080009e6(void)

{
  byte bVar1;
  char cVar2;
  char cVar3;
  short sVar4;
  int *piVar5;
  undefined1 uVar6;
  int iVar7;
  uint *puVar8;
  uint uVar9;
  uint uVar10;
  int *piVar11;
  byte *pbVar12;
  undefined2 uVar13;
  
  piVar5 = DAT_08000bb4;
  cVar2 = (char)DAT_08000bb4[0x11];
  switch((char)DAT_08000bb4[0x2a]) {
  case '\0':
  case '\x03':
    goto switchD_08000a06_caseD_0;
  case '\x01':
    pbVar12 = (byte *)(DAT_08000bb4 + 6);
    bVar1 = *(byte *)(DAT_08000bb4 + 6);
    piVar11 = (int *)0x0;
    cVar2 = *(char *)((int)DAT_08000bb4 + 0x19);
    uVar9 = bVar1 & 0x1f;
    if ((bVar1 & 0x60) != 0) {
      if ((((uint)bVar1 << 0x19) >> 0x1e != 1 || uVar9 != 1) || (cVar2 != '\n'))
      goto switchD_08000a4c_caseD_2;
      piVar11 = (int *)((int)DAT_08000bb4 + 0xaa);
LAB_08000ab6:
      uVar9 = 1;
      goto LAB_08000ab8;
    }
    cVar3 = *(char *)((int)DAT_08000bb4 + 0x1b);
    if ((bVar1 & 0x1f) != 0) {
      if (uVar9 == 1) {
        if (cVar2 != '\x06' || cVar3 != '\v') goto switchD_08000a4c_caseD_2;
      }
      else {
        if (uVar9 != 2) goto switchD_08000a4c_caseD_2;
        if (cVar2 == '\0') {
          if ((*(byte *)(DAT_08000bb4 + 7) & 0x7f) < 4) {
            piVar11 = (int *)FUN_080026c8();
            iVar7 = -((*piVar11 << 10) >> 0x1f);
            if (iVar7 != 0) {
              iVar7 = 1;
            }
            *(short *)(piVar5 + 8) = (short)iVar7;
            piVar11 = piVar5 + 8;
            uVar9 = 2;
            goto LAB_08000ab8;
          }
          goto switchD_08000a4c_caseD_2;
        }
        if (cVar2 == '\x01') {
          if (*(short *)((int)DAT_08000bb4 + 0x1a) != 0) goto switchD_08000a4c_caseD_2;
          puVar8 = (uint *)FUN_080026c8();
          uVar9 = *puVar8 & 0xffdfffff;
          uVar10 = (uVar9 << 0xc) >> 0x1e;
          if (uVar10 == 3 || uVar10 == 2) {
            uVar9 = uVar9 | 0x10000000;
          }
          *puVar8 = uVar9;
        }
        else {
          if (cVar2 != '\x03' || *(short *)((int)DAT_08000bb4 + 0x1a) != 0)
          goto switchD_08000a4c_caseD_2;
          puVar8 = (uint *)FUN_080026c8();
          uVar9 = *puVar8;
          if ((uVar9 & 0x80000000) != 0) {
            uVar9 = uVar9 | 0x40000000;
          }
          *puVar8 = uVar9 | 0x200000;
        }
      }
      goto switchD_08000a4c_caseD_1;
    }
    switch(cVar2) {
    case '\0':
      uVar13 = 0;
      if (((code *)DAT_08000bb4[2] != (code *)0x0) &&
         (iVar7 = (*(code *)DAT_08000bb4[2])(), iVar7 != 0)) {
        uVar13 = 1;
      }
      *(undefined2 *)(piVar5 + 8) = uVar13;
      piVar11 = piVar5 + 8;
      uVar9 = 2;
      goto LAB_08000ab8;
    case '\x01':
      break;
    default:
switchD_08000a4c_caseD_2:
      puVar8 = (uint *)FUN_080026c8(0x80);
      uVar9 = *puVar8;
      if ((uVar9 & 0x80000000) != 0) {
        uVar9 = uVar9 | 0x40000000;
      }
      *puVar8 = uVar9 | 0x200000;
      puVar8 = (uint *)FUN_080026c8(0);
      uVar9 = *puVar8;
      if ((uVar9 & 0x80000000) != 0) {
        uVar9 = uVar9 | 0x40000000;
      }
      *puVar8 = uVar9 | 0x200000;
      *(undefined1 *)(piVar5 + 0x2a) = 6;
      return;
    case '\x05':
      *(uint *)(*DAT_08000bb4 + 0x800) =
           *(uint *)(*DAT_08000bb4 + 0x800) & 0xfffff80f |
           (*(byte *)((int)DAT_08000bb4 + 0x1a) & 0x7f) << 4;
      FUN_0800042e(3);
      break;
    case '\x06':
      if (cVar3 != '\x01') {
        if (cVar3 == '\x02') {
          piVar11 = (int *)DAT_08000bb4[4];
          uVar9 = DAT_08000bb4[5];
          if (uVar9 != 0xffffffff) goto LAB_08000ab8;
        }
        goto switchD_08000a4c_caseD_2;
      }
      piVar11 = (int *)DAT_08000bb4[3];
      uVar9 = 0x12;
      goto LAB_08000ab8;
    case '\b':
      piVar11 = (int *)((int)DAT_08000bb4 + 0xa9);
      goto LAB_08000ab6;
    case '\t':
      FUN_08000954(*(undefined1 *)((int)DAT_08000bb4 + 0x1a));
    }
switchD_08000a4c_caseD_1:
    uVar9 = 0;
LAB_08000ab8:
    if ((*pbVar12 & 0x80) != 0) {
      if (*(ushort *)((int)piVar5 + 0x1e) < uVar9) {
        uVar9 = (uint)*(ushort *)((int)piVar5 + 0x1e);
      }
      if (uVar9 == 0) {
        *(undefined1 *)(piVar5 + 0x2a) = 4;
      }
      else {
        FUN_0800078e(0x80,piVar11,uVar9,uVar9);
        *(undefined1 *)(piVar5 + 0x2a) = 2;
      }
      FUN_0800078e(0,0,0);
      return;
    }
    sVar4 = *(short *)((int)piVar5 + 0x1e);
    if (sVar4 == 0) {
      uVar6 = 5;
    }
    else {
      FUN_0800078e(0,piVar11,sVar4,sVar4);
      uVar6 = 3;
    }
    *(undefined1 *)(piVar5 + 0x2a) = uVar6;
    FUN_0800078e(0x80,0,0);
    return;
  case '\x02':
    if ((char)DAT_08000bb4[0xd] == '\x02') {
      *(undefined1 *)(DAT_08000bb4 + 0x2a) = 4;
      puVar8 = (uint *)FUN_080026c8(0x80);
      uVar9 = *puVar8;
      if ((uVar9 & 0x80000000) != 0) {
        uVar9 = uVar9 | 0x40000000;
      }
      *puVar8 = uVar9 | 0x200000;
      return;
    }
    if (cVar2 != '\x02') {
      return;
    }
    *(undefined1 *)(DAT_08000bb4 + 0x2a) = 4;
    FUN_08000862(0x80);
    return;
  case '\x04':
    break;
  case '\x05':
    cVar2 = (char)DAT_08000bb4[0xd];
    break;
  default:
    return;
  }
  if (cVar2 == '\x02') {
    *(undefined1 *)(DAT_08000bb4 + 0x2a) = 0;
  }
switchD_08000a06_caseD_0:
  return;
}



/* ===== FUN_08000c2c @ 08000c2c | callers: FUN_080014b4 ===== */

void FUN_08000c2c(void)

{
  int *piVar1;
  uint *puVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  bool bVar7;
  
  piVar1 = DAT_08000d4c;
  uVar5 = *(uint *)(*DAT_08000d4c + 0x14);
  uVar6 = *(uint *)(*DAT_08000d4c + 4);
  if (uVar6 != 0) {
    if ((uVar6 & 4) != 0) {
      FUN_0800042e(0);
    }
    *(uint *)(*piVar1 + 4) = uVar6;
  }
  if (uVar5 == 0) {
    return;
  }
  if (((uVar5 & 0x10000000) != 0) && (puVar2 = (uint *)*piVar1, (*puVar2 & 0x10000) != 0)) {
    puVar2[0x200] = puVar2[0x200] | 3;
    iVar3 = DAT_08000d50;
    do {
      bVar7 = iVar3 != 0;
      iVar3 = iVar3 + -1;
    } while (bVar7);
  }
  if ((uVar5 & 1) != 0) {
    return;
  }
  if ((uVar5 & 0x40000000) != 0) {
    FUN_0800042e(1);
  }
  if ((uVar5 & 0x800) != 0) {
    *(undefined1 *)(piVar1 + 0x2b) = *(undefined1 *)((int)piVar1 + 0xab);
    FUN_0800042e(5);
  }
  if ((uVar5 & 0x80000000) != 0) {
    FUN_0800042e((char)piVar1[0x2b]);
  }
  if ((uVar5 & 0x1000) != 0) {
    FUN_08000446();
  }
  if ((uVar5 & 0x2000) == 0) goto LAB_08000cf2;
  iVar3 = *piVar1;
  uVar6 = *(uint *)(iVar3 + 0x900);
  uVar4 = (uint)(*(int *)(iVar3 + 0x808) << 0x1d) >> 0x1e;
  if (uVar4 < 2) {
LAB_08000cdc:
    uVar6 = uVar6 & 0xfffffffc;
    *(uint *)(iVar3 + 0xc) = (*(uint *)(iVar3 + 0xc) & 0xffffc3ff) + 0x2400;
  }
  else if (uVar4 == 2) {
    uVar6 = uVar6 | 3;
  }
  else if (uVar4 == 3) goto LAB_08000cdc;
  *(uint *)(*piVar1 + 0x900) = uVar6;
LAB_08000cf2:
  FUN_0800055e();
  FUN_080009e6();
  *(uint *)(*piVar1 + 0x14) = uVar5 & 0xffffffef;
  return;
}



/* ===== FUN_08000d04 @ 08000d04 | callers: FUN_08001986 ===== */

void FUN_08000d04(int *param_1)

{
  int *piVar1;
  int iVar2;
  bool bVar3;
  
  piVar1 = DAT_08000d4c;
  DAT_08000d4c[1] = *param_1;
  piVar1[2] = param_1[1];
  piVar1[3] = param_1[2];
  piVar1[4] = param_1[3];
  piVar1[5] = param_1[4];
  *piVar1 = 0x50000000;
  FUN_0800039c();
  *(uint *)(*piVar1 + 0xc) = *(uint *)(*piVar1 + 0xc) & 0xdffffcff | 0x40000000;
  iVar2 = DAT_08000d54;
  do {
    bVar3 = iVar2 != 0;
    iVar2 = iVar2 + -1;
  } while (bVar3);
  FUN_0800042e(0);
  return;
}



/* ===== FUN_08000d58 @ 08000d58 | callers: FUN_08001338 ===== */

void FUN_08000d58(void)

{
  uint *puVar1;
  
  puVar1 = DAT_08001138;
  *DAT_08001138 = *DAT_08001138 | 0x10000;
  do {
  } while (-1 < (int)(*puVar1 << 0xe));
  *DAT_0800113c = 0x12;
  puVar1[1] = 0xc400;
  puVar1[0xb] = DAT_08001140;
  *puVar1 = *puVar1 | 0x4000000;
  do {
  } while (-1 < (int)(*puVar1 << 4));
  puVar1[1] = puVar1[1] & 0xffc0ffff;
  puVar1[1] = puVar1[1] | 0x1d0000;
  *puVar1 = *puVar1 | 0x1000000;
  do {
  } while (-1 < (int)(*puVar1 << 6));
  puVar1[1] = puVar1[1] & 0xfffffffc;
  puVar1[1] = puVar1[1] | 2;
  do {
  } while ((puVar1[1] << 0x1c) >> 0x1e != 2);
  puVar1[1] = puVar1[1] & 0xffbf3fff;
  return;
}



/* ===== FUN_08000dcc @ 08000dcc | callers: FUN_08001338 ===== */

void FUN_08000dcc(void)

{
  int iVar1;
  uint uVar2;
  
  iVar1 = DAT_08001138;
  *(uint *)(DAT_08001138 + 0x28) = *(uint *)(DAT_08001138 + 0x28) | 0x1000;
  *(uint *)(iVar1 + 0x14) = *(uint *)(iVar1 + 0x14) | 0x1041;
  *(uint *)(iVar1 + 0x28) = *(uint *)(iVar1 + 0x28) & 0xffffefff;
  *(uint *)(iVar1 + 0xc) = *(uint *)(iVar1 + 0xc) | 0xe7d;
  *(undefined4 *)(iVar1 + 0x18) = 0xe7d;
  *(uint *)(iVar1 + 0xc) = *(uint *)(iVar1 + 0xc) & 0xfffff182;
  uVar2 = DAT_08001144;
  *(uint *)(iVar1 + 0x10) = *(uint *)(iVar1 + 0x10) | DAT_08001144;
  *(uint *)(iVar1 + 0x1c) = *(uint *)(iVar1 + 0x1c) | uVar2;
  *(uint *)(iVar1 + 0x10) = *(uint *)(iVar1 + 0x10) & ~DAT_08001144;
  return;
}



/* ===== FUN_08000e14 @ 08000e14 | callers: FUN_08001338 ===== */

void FUN_08000e14(void)

{
  undefined4 *puVar1;
  
  *(uint *)(DAT_08001148 + 4) = *(uint *)(DAT_08001148 + 4) & 0xf8ffffff | 0x4000000;
  *(uint *)(DAT_0800114c + 4) = *(uint *)(DAT_0800114c + 4) & 0xffffff1f;
  *DAT_08001150 = 0xa012;
  puVar1 = DAT_08001150;
  DAT_08001150[-3] = DAT_08001154;
  puVar1[-2] = DAT_08001158;
  *DAT_0800115c = 0x6a52;
  puVar1 = DAT_0800115c;
  DAT_0800115c[-3] = DAT_08001160;
  puVar1[-2] = DAT_08001164;
  puVar1 = DAT_08001168;
  DAT_08001168[3] = 0;
  *puVar1 = DAT_0800116c;
  puVar1[1] = 0x33333333;
  *DAT_08001170 = 0xfffb;
  puVar1 = DAT_08001170;
  DAT_08001170[-3] = DAT_08001174;
  puVar1[-2] = 0x88888888;
  *DAT_08001178 = 0;
  puVar1 = DAT_08001178;
  DAT_08001178[-3] = 0x33333333;
  puVar1[-2] = 0x33333333;
  *DAT_0800117c = 0x10000;
  DAT_0800117c[5] = 0xe10;
  return;
}



/* ===== FUN_08000ea2 @ 08000ea2 | callers: FUN_08001072,FUN_08001338 ===== */

void FUN_08000ea2(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  iVar1 = 0x8000;
  puVar2 = (undefined4 *)(DAT_08001150 + 4);
  *puVar2 = 0x4000000;
  do {
    iVar1 = iVar1 + -1;
  } while (iVar1 != 0);
  *puVar2 = 0x400;
  return;
}



/* ===== FUN_08000ebe @ 08000ebe | callers: FUN_08000ef2,FUN_08000f3e,FUN_080011a8 ===== */

int FUN_08000ebe(undefined2 *param_1,int param_2)

{
  undefined2 uVar1;
  uint uVar2;
  int iVar3;
  
  iVar3 = 0;
  uVar2 = 0;
  do {
    if (param_2 == 0) {
      uVar1 = FUN_08001af6(uVar2);
      *param_1 = uVar1;
    }
    else {
      iVar3 = FUN_08001b1c(uVar2,*param_1);
      if (iVar3 != 0) {
        return iVar3;
      }
    }
    param_1 = param_1 + 1;
    uVar2 = uVar2 + 1;
  } while (uVar2 < 0x10);
  return iVar3;
}



/* ===== FUN_08000ef2 @ 08000ef2 | callers: FUN_080010aa ===== */

undefined4 FUN_08000ef2(int param_1)

{
  char cVar1;
  int iVar2;
  undefined1 auStack_30 [4];
  undefined4 local_2c;
  
  FUN_08000ebe(auStack_30,0);
  *(undefined4 *)(param_1 + 4) = DAT_08000180;
  iVar2 = DAT_08001180;
  *(undefined4 *)(param_1 + 8) = 0;
  *(undefined4 *)(param_1 + 0xc) = 0;
  cVar1 = *(char *)(iVar2 + 0xc);
  if (((cVar1 != '\x01') && (cVar1 != '\x02')) && (cVar1 != '\x03')) {
    local_2c = 0xffffffff;
  }
  *(undefined4 *)(param_1 + 0x10) = local_2c;
  *(undefined1 *)(param_1 + 0x14) = 2;
  *(undefined1 *)(param_1 + 0x15) = 3;
  *(undefined2 *)(param_1 + 1) = 0x12;
  return 0;
}



/* ===== FUN_08000f3e @ 08000f3e | callers:  ===== */

undefined4 FUN_08000f3e(int param_1)

{
  uint *puVar1;
  uint uVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  uint uVar6;
  
  puVar1 = DAT_08001180;
  iVar5 = *(int *)(param_1 + 0x10);
  if ((char)DAT_08001180[3] == '\x03') {
    uVar4 = 8;
  }
  else {
    FUN_08001a12();
    uVar2 = DAT_08001184;
    uVar6 = iVar5 + DAT_08001184;
    for (uVar3 = DAT_08001184; uVar3 < uVar6; uVar3 = uVar3 + 0x800) {
      iVar5 = FUN_08001a7a(uVar3);
      if (iVar5 != 0) goto LAB_08000f80;
    }
    iVar5 = FUN_08000ebe(param_1 + 8,1);
    if (iVar5 == 0) {
      *(undefined1 *)(puVar1 + 3) = 5;
      *puVar1 = uVar2;
      puVar1[2] = *(uint *)(param_1 + 4);
      puVar1[1] = DAT_08001188;
      *(undefined4 *)(param_1 + 4) = 0x800;
      *(undefined2 *)(param_1 + 1) = 4;
      return 0;
    }
LAB_08000f80:
    uVar4 = 6;
  }
  FUN_08001a1e();
  return uVar4;
}



/* ===== FUN_08000fb0 @ 08000fb0 | callers: FUN_08001004 ===== */

void FUN_08000fb0(int *param_1,uint param_2)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  bool bVar7;
  
  iVar1 = DAT_08001180;
  param_2 = param_2 >> 2;
  uVar5 = *(uint *)(DAT_08001180 + 4);
  uVar4 = *(uint *)(DAT_08001180 + 8);
  while (bVar7 = param_2 != 0, param_2 = param_2 - 1, bVar7) {
    iVar6 = *param_1;
    iVar2 = FUN_080026c0(((iVar6 - uVar5 ^ DAT_0800118c) + uVar4 * 2 ^ uVar4) + uVar4 * -8,0x11);
    *param_1 = iVar2;
    uVar4 = uVar4 + uVar5 * 8;
    uVar4 = uVar4 ^ uVar4 >> 1;
    uVar3 = FUN_080026c0(iVar6,7);
    uVar5 = (uVar3 ^ uVar5) + DAT_08001190;
    param_1 = param_1 + 1;
  }
  *(uint *)(iVar1 + 4) = uVar5;
  *(uint *)(iVar1 + 8) = uVar4;
  return;
}



/* ===== FUN_08001004 @ 08001004 | callers: FUN_080010aa ===== */

undefined4 FUN_08001004(int param_1)

{
  int *piVar1;
  int iVar2;
  undefined2 *puVar3;
  uint uVar4;
  undefined4 uVar5;
  
  piVar1 = DAT_08001180;
  uVar5 = 0;
  if ((*(short *)(param_1 + 1) == 0x800) && ((uint)(*DAT_08001180 + DAT_08001194) < 0xc001)) {
    FUN_08000fb0(param_1 + 4);
    uVar4 = 0;
    puVar3 = (undefined2 *)(param_1 + 4);
    do {
      iVar2 = FUN_08001a82(*piVar1,*puVar3);
      if (iVar2 != 0) {
        uVar5 = 6;
        break;
      }
      uVar4 = uVar4 + 1;
      *piVar1 = *piVar1 + 2;
      puVar3 = puVar3 + 1;
    } while (uVar4 < 0x400);
  }
  else {
    uVar5 = 1;
  }
  *(undefined2 *)(param_1 + 1) = 0;
  return uVar5;
}



/* ===== FUN_08001064 @ 08001064 | callers: FUN_080010aa ===== */

void FUN_08001064(void)

{
  FUN_08001a1e();
  *(undefined1 *)(DAT_08001180 + 0xc) = 0;
  return;
}



/* ===== FUN_08001072 @ 08001072 | callers: FUN_080010aa ===== */

undefined4 FUN_08001072(void)

{
  if (*(char *)(DAT_08001180 + 0xc) != '\x03') {
    FUN_08000ea2();
    FUN_08000218(DAT_08001198);
    return 0;
  }
  return 8;
}



/* ===== FUN_0800108e @ 0800108e | callers: FUN_080010aa ===== */

undefined4 FUN_0800108e(void)

{
  char cVar1;
  
  cVar1 = *(char *)(DAT_08001180 + 0xc);
  if (cVar1 == '\x01') {
    *(undefined1 *)(DAT_08001180 + 0xc) = 2;
  }
  else if ((cVar1 != '\x02') && (cVar1 != '\x03')) {
    return 8;
  }
  return 0;
}



/* ===== FUN_080010aa @ 080010aa | callers: FUN_080012f4,FUN_0800122a ===== */

undefined1 * FUN_080010aa(void)

{
  undefined1 *puVar1;
  int iVar2;
  undefined1 *puVar3;
  
  puVar3 = (undefined1 *)0x1;
  puVar1 = (undefined1 *)FUN_08001708();
  if (puVar1 == (undefined1 *)0x0) {
    return (undefined1 *)0x0;
  }
  iVar2 = FUN_08001750();
  if ((iVar2 != 0) && (iVar2 = FUN_08001740(), iVar2 != 0)) {
    puVar3 = (undefined1 *)0x5;
    goto switchD_080010d2_caseD_84;
  }
  switch(*puVar1) {
  case 0x80:
    puVar3 = puVar1;
    goto LAB_08001110;
  case 0x81:
    puVar3 = (undefined1 *)FUN_08001004(puVar1);
    break;
  case 0x82:
    puVar3 = (undefined1 *)FUN_08001064();
    break;
  case 0x83:
    puVar3 = (undefined1 *)FUN_08000ef2(puVar1);
    break;
  case 0x84:
    goto switchD_080010d2_caseD_84;
  default:
    if (*(char *)(DAT_080013f8 + 0xc) == '\x03') {
      return puVar1;
    }
    goto switchD_080010d2_caseD_84;
  case 0x86:
    puVar3 = (undefined1 *)0x0;
    goto LAB_0800112e;
  case 0x87:
    puVar3 = (undefined1 *)FUN_08001072(puVar1);
LAB_08001110:
    if (puVar3 == &NMI) {
      FUN_0800176c();
      return (undefined1 *)0xffffffff;
    }
    break;
  case 0x88:
    puVar3 = (undefined1 *)FUN_0800108e(puVar1);
    break;
  case 0x89:
    puVar3 = (undefined1 *)FUN_08001362(puVar1);
  }
  if (puVar3 != (undefined1 *)0x0) {
switchD_080010d2_caseD_84:
    *(undefined2 *)(puVar1 + 1) = 0;
  }
LAB_0800112e:
  *puVar1 = (char)puVar3;
  FUN_08001784();
  return (undefined1 *)0x0;
}



/* ===== FUN_080011a8 @ 080011a8 | callers: FUN_080012f4 ===== */

undefined4 FUN_080011a8(void)

{
  undefined4 local_28;
  uint local_24;
  uint local_20;
  
  FUN_08000ebe(&local_28,0);
  if (((local_20 != 0) && (local_20 < 0xc001)) && (0x5ff < local_24)) {
    FUN_08001a98(DAT_080013fc,local_20 >> 2);
  }
  return 1;
}



/* ===== FUN_080011f6 @ 080011f6 | callers: FUN_0800126a,FUN_080012f4,FUN_0800122a,FUN_08001286,FUN_0800125a,FUN_08001248,FUN_0800123a ===== */

void FUN_080011f6(void)

{
  int iVar1;
  uint uVar2;
  undefined4 uVar3;
  
  FUN_080018a6();
  iVar1 = DAT_080013f8;
  if ((*(char *)(DAT_080013f8 + 0xc) != '\x03') && (*(int *)(DAT_080013f8 + 0x10) == 0)) {
    uVar3 = 0x2000;
    uVar2 = FUN_08002590();
    if (uVar2 < 8000) {
      uVar3 = 0x20000000;
    }
    *DAT_08001400 = uVar3;
    *(undefined4 *)(iVar1 + 0x10) = 10000;
  }
  *(int *)(iVar1 + 0x10) = *(int *)(iVar1 + 0x10) + -1;
  return;
}



/* ===== FUN_0800122a @ 0800122a | callers:  ===== */

void FUN_0800122a(undefined4 *param_1)

{
  undefined4 uVar1;
  
  FUN_080011f6();
  uVar1 = FUN_080010aa();
  *param_1 = uVar1;
  return;
}



/* ===== FUN_0800123a @ 0800123a | callers:  ===== */

void FUN_0800123a(void)

{
  FUN_080011f6();
  FUN_08001784();
  return;
}



/* ===== FUN_08001248 @ 08001248 | callers:  ===== */

void FUN_08001248(undefined4 *param_1)

{
  undefined4 uVar1;
  
  FUN_080011f6();
  uVar1 = FUN_0800179c(*param_1);
  *param_1 = uVar1;
  return;
}



/* ===== FUN_0800125a @ 0800125a | callers:  ===== */

void FUN_0800125a(undefined4 *param_1)

{
  undefined4 uVar1;
  
  FUN_080011f6();
  uVar1 = FUN_08001828();
  *param_1 = uVar1;
  return;
}



/* ===== FUN_0800126a @ 0800126a | callers:  ===== */

void FUN_0800126a(undefined4 *param_1)

{
  FUN_080011f6();
  FUN_08001976(*param_1,param_1[1],param_1[2]);
  *(undefined4 *)(DAT_080019c4 + 0x1c) = param_1[3];
  return;
}



/* ===== FUN_08001286 @ 08001286 | callers:  ===== */

void FUN_08001286(undefined4 *param_1)

{
  undefined4 uVar1;
  
  FUN_080011f6();
  uVar1 = FUN_08001738();
  *param_1 = uVar1;
  return;
}



/* ===== FUN_08001298 @ 08001298 | callers:  ===== */

void FUN_08001298(int *param_1)

{
  undefined2 uVar1;
  
  uVar1 = FUN_08001af6(*param_1 + 0x40);
  *(undefined2 *)param_1 = uVar1;
  return;
}



/* ===== FUN_080012a8 @ 080012a8 | callers:  ===== */

void FUN_080012a8(uint *param_1)

{
  int iVar1;
  
  iVar1 = FUN_08001b1c(*param_1 + 0x40,(short)param_1[1]);
  *param_1 = (uint)(iVar1 == 0);
  return;
}



/* ===== FUN_080012e4 @ 080012e4 | callers:  ===== */

void FUN_080012e4(undefined4 *param_1)

{
  undefined4 uVar1;
  
  uVar1 = FUN_08001a98(*param_1,param_1[1]);
  *param_1 = uVar1;
  return;
}



/* ===== FUN_080012f4 @ 080012f4 | callers: FUN_08001338 ===== */

void FUN_080012f4(void)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  
  uVar2 = DAT_080013fc;
  iVar1 = DAT_080013f8;
  do {
    FUN_080011f6();
    if (*(char *)(iVar1 + 0xc) == '\0') {
      iVar3 = FUN_080011a8();
      if (iVar3 == 0) goto LAB_08001318;
      *(undefined1 *)(iVar1 + 0xc) = 1;
    }
    else if (*(char *)(iVar1 + 0xc) == '\x02') {
      *(undefined1 *)(iVar1 + 0xc) = 3;
      FUN_08000218(uVar2);
LAB_08001318:
      *(undefined1 *)(iVar1 + 0xc) = 4;
    }
    FUN_080010aa();
  } while( true );
}



/* ===== FUN_08001338 @ 08001338 | callers: thunk_FUN_08001338 ===== */

undefined4 FUN_08001338(void)

{
  char cVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uStack_1c;
  int iStack_18;
  
  FUN_08000dcc();
  FUN_08000e14();
  FUN_08000d58();
  FUN_080023da();
  FUN_08001986(DAT_08001404);
  FUN_08001ac0();
  FUN_08000ea2();
  iVar2 = DAT_080013f8;
  *(undefined1 *)(DAT_080013f8 + 0xc) = 0;
  *(undefined4 *)(iVar2 + 0x10) = 0;
  iVar2 = FUN_080012f4();
  uVar4 = 0;
  if (*(ushort *)(iVar2 + 1) < 0xd) {
LAB_08001386:
    uVar4 = 1;
  }
  else {
    cVar1 = *(char *)(iVar2 + 4);
    if ((cVar1 != '\x01') && (cVar1 != '\x02')) {
      if (cVar1 == '\x03') {
        uStack_1c = 0;
        iStack_18 = 0;
        iVar3 = FUN_08002146(iVar2 + 0x11,*(ushort *)(iVar2 + 1) - 0xd,*(undefined2 *)(iVar2 + 0xb),
                             &uStack_1c,iVar2 + 6,*(undefined2 *)(iVar2 + 9),
                             *(undefined2 *)(iVar2 + 0xd),*(undefined2 *)(iVar2 + 0xf),&iStack_18);
        if (iVar3 != 0) {
          *(short *)(iVar2 + 4) = (short)uStack_1c;
          *(short *)(iVar2 + 1) = (short)(iStack_18 << 1) + 2;
          return 0;
        }
        return 6;
      }
      if (cVar1 != '\x04') goto LAB_08001386;
    }
    FUN_0800211a(cVar1 != '\x04',*(undefined4 *)(iVar2 + 5),cVar1 == '\x02');
  }
  return uVar4;
}



/* ===== FUN_08001362 @ 08001362 | callers: FUN_080010aa ===== */

undefined4 FUN_08001362(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uStack_1c;
  int iStack_18;
  
  uVar3 = 0;
  if (*(ushort *)(param_1 + 1) < 0xd) {
LAB_08001386:
    uVar3 = 1;
  }
  else {
    cVar1 = *(char *)(param_1 + 4);
    if ((cVar1 != '\x01') && (cVar1 != '\x02')) {
      if (cVar1 == '\x03') {
        uStack_1c = 0;
        iStack_18 = 0;
        iVar2 = FUN_08002146(param_1 + 0x11,*(ushort *)(param_1 + 1) - 0xd,
                             *(undefined2 *)(param_1 + 0xb),&uStack_1c,param_1 + 6,
                             *(undefined2 *)(param_1 + 9),*(undefined2 *)(param_1 + 0xd),
                             *(undefined2 *)(param_1 + 0xf),&iStack_18);
        if (iVar2 != 0) {
          *(short *)(param_1 + 4) = (short)uStack_1c;
          *(short *)(param_1 + 1) = (short)(iStack_18 << 1) + 2;
          return 0;
        }
        return 6;
      }
      if (cVar1 != '\x04') goto LAB_08001386;
    }
    FUN_0800211a(cVar1 != '\x04',*(undefined4 *)(param_1 + 5),cVar1 == '\x02');
  }
  return uVar3;
}



/* ===== FUN_08001408 @ 08001408 | callers:  ===== */

void FUN_08001408(int param_1)

{
  byte *pbVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  byte bVar6;
  
  iVar2 = DAT_08001804;
  pbVar1 = (byte *)(DAT_08001804 + 0xe);
  if ((param_1 != 4) && (*pbVar1 == 8)) {
    *(byte *)(DAT_08001804 + 0xf) = *(byte *)(DAT_08001804 + 0xf) | 0x80;
  }
  uVar3 = *pbVar1 - 6;
  uVar4 = uVar3;
  if (uVar3 < 5) {
    uVar4 = 0;
  }
  if (uVar3 < 5) {
    *(char *)(iVar2 + 0xe) = (char)uVar4;
  }
  *(byte *)(iVar2 + 0xf) = *(byte *)(iVar2 + 0xf) & 0xfd;
  if (*(int *)(iVar2 + 0x1c) == 0) {
    return;
  }
  iVar5 = FUN_0800043e();
  bVar6 = iVar5 == 4;
  iVar5 = FUN_0800210c();
  if (iVar5 != 0) {
    bVar6 = bVar6 | 2;
  }
                    /* WARNING: Could not recover jumptable at 0x08001458. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(iVar2 + 0x1c))(bVar6);
  return;
}



/* ===== FUN_0800145a @ 0800145a | callers:  ===== */

void FUN_0800145a(int param_1)

{
  char *pcVar1;
  int iVar2;
  int iVar3;
  byte bVar4;
  
  iVar2 = DAT_08001804;
  pcVar1 = (char *)(DAT_08001804 + 0xe);
  if (param_1 == 0 && *pcVar1 == '\x03') {
    *(byte *)(DAT_08001804 + 0xf) = *(byte *)(DAT_08001804 + 0xf) | 0x80;
  }
  switch(*pcVar1) {
  case '\x01':
  case '\x02':
  case '\x03':
  case '\x04':
  case '\x05':
    *(undefined1 *)(iVar2 + 0xe) = 0;
  }
  *(byte *)(iVar2 + 0xf) = *(byte *)(iVar2 + 0xf) & 0xfe;
  if (*(int *)(iVar2 + 0x1c) == 0) {
    return;
  }
  iVar3 = FUN_0800043e();
  bVar4 = iVar3 == 4;
  iVar3 = FUN_0800210c();
  if (iVar3 != 0) {
    bVar4 = bVar4 | 2;
  }
                    /* WARNING: Could not recover jumptable at 0x080014b2. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(iVar2 + 0x1c))(bVar4);
  return;
}



/* ===== FUN_080014b4 @ 080014b4 | callers: FUN_0800179c,FUN_080018a6 ===== */

void FUN_080014b4(void)

{
  char cVar1;
  ushort uVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  bool bVar8;
  
  FUN_08000c2c();
  iVar4 = FUN_0800043e();
  puVar3 = DAT_08001804;
  if (iVar4 != 4) {
    return;
  }
  cVar1 = *(char *)((int)DAT_08001804 + 0xe);
  if (cVar1 == '\0') {
    iVar4 = FUN_0800093c(2);
    if (iVar4 == 0) {
      uVar7 = 0x40;
      iVar4 = 0x40;
      puVar6 = puVar3 + 9;
      uVar5 = 2;
LAB_080015a4:
      FUN_0800078e(uVar5,puVar6,iVar4,uVar7);
    }
    else if (((iVar4 != 1) && (iVar4 == 2)) &&
            (FUN_08000862(2),
            ((*(ushort *)((int)puVar3 + 0x25) >> 8) + 0x55 +
             (ushort)*(byte *)(puVar3 + 9) + *(ushort *)((int)puVar3 + 0x25) & 0xff) ==
            (ushort)*(byte *)((int)puVar3 + 0x27))) {
      iVar4 = 0xf;
      do {
        bVar8 = iVar4 != 0;
        *(undefined4 *)((int)puVar3 + iVar4 * 4 + 0x29a) = puVar3[iVar4 + 9];
        iVar4 = iVar4 + -1;
      } while (bVar8);
      if (*(ushort *)((int)puVar3 + 0x29b) < 0x3d) {
        *(undefined1 *)((int)puVar3 + 0xe) = 7;
      }
      else {
        FUN_0800078e(2,(int)puVar3 + 0x2da,*(ushort *)((int)puVar3 + 0x29b) - 0x3c,0xfd2);
        *(undefined1 *)((int)puVar3 + 0xe) = 6;
        *puVar3 = puVar3[5];
      }
    }
  }
  else if (cVar1 == '\x06') {
    iVar4 = FUN_0800093c(2);
    if (iVar4 == 0) {
LAB_080015c0:
      *(undefined1 *)((int)puVar3 + 0xe) = 0;
    }
    else if ((iVar4 != 1) && (iVar4 == 2)) {
      FUN_08000862();
      *(undefined1 *)((int)puVar3 + 0xe) = 7;
    }
  }
  else {
    if (cVar1 == '\t') {
      if ((*(byte *)((int)DAT_08001804 + 0xf) & 2) != 0) goto LAB_080015ce;
      uVar2 = *(ushort *)((int)DAT_08001804 + 0x29b);
      *(char *)((int)DAT_08001804 + 0x29d) =
           *(char *)((int)DAT_08001804 + 0x29a) + (char)uVar2 + (char)(uVar2 >> 8) + 'U';
      *(undefined1 *)((int)puVar3 + 0xe) = 10;
      *puVar3 = puVar3[4];
      iVar4 = uVar2 + 4;
      uVar7 = 0x1012;
      uVar5 = 0x81;
      puVar6 = (undefined4 *)((int)puVar3 + 0x29a);
      goto LAB_080015a4;
    }
    if (cVar1 == '\n') {
      iVar4 = FUN_0800093c(0x81);
      if (iVar4 == 0) goto LAB_080015c0;
      if (iVar4 == 2) {
        FUN_08000862(0x81);
        *(undefined1 *)((int)puVar3 + 0xe) = 0;
      }
    }
  }
  if ((*(byte *)((int)puVar3 + 0xf) & 2) == 0) {
    return;
  }
LAB_080015ce:
  iVar4 = FUN_0800093c(0x81);
  if (iVar4 != 2) {
    return;
  }
  FUN_08000862(0x81);
  *(byte *)((int)puVar3 + 0xf) = *(byte *)((int)puVar3 + 0xf) & 0xfd;
  return;
}



/* ===== FUN_080015ee @ 080015ee | callers: FUN_0800179c,FUN_080018a6 ===== */

void FUN_080015ee(void)

{
  char cVar1;
  ushort uVar2;
  undefined4 *puVar3;
  undefined2 uVar4;
  int iVar5;
  
  FUN_0800221a();
  iVar5 = FUN_0800210c();
  puVar3 = DAT_08001804;
  if (iVar5 == 0) {
    return;
  }
  cVar1 = *(char *)((int)DAT_08001804 + 0xe);
  if (cVar1 == '\0') {
    iVar5 = FUN_080020ae();
    if (iVar5 == 0) {
      FUN_08002094(puVar3 + 8,4);
    }
    else if (iVar5 == 2) {
      FUN_08002102();
      uVar2 = *(ushort *)((int)puVar3 + 0x21);
      if (((*(byte *)(puVar3 + 8) + uVar2 + (uVar2 >> 8) + 0x55 & 0xff) ==
           (ushort)*(byte *)((int)puVar3 + 0x23)) && (uVar2 < 0x100e)) {
        *(undefined4 *)((int)puVar3 + 0x29a) = puVar3[8];
        if (uVar2 == 0) {
          *(undefined1 *)((int)puVar3 + 0xe) = 2;
        }
        else {
          FUN_08002094((int)puVar3 + 0x29e);
          *(undefined1 *)((int)puVar3 + 0xe) = 1;
          *puVar3 = puVar3[5];
          uVar4 = FUN_080020ea();
          *(undefined2 *)((int)puVar3 + 10) = uVar4;
        }
      }
    }
  }
  else if (cVar1 == '\x01') {
    iVar5 = FUN_080020ae();
    if (iVar5 == 0) {
LAB_080016de:
      *(undefined1 *)((int)puVar3 + 0xe) = 0;
    }
    else if (iVar5 == 2) {
      FUN_08002102();
      *(undefined1 *)((int)puVar3 + 0xe) = 2;
    }
  }
  else if (cVar1 == '\x04') {
    if ((*(byte *)((int)DAT_08001804 + 0xf) & 1) != 0) goto LAB_080016ec;
    *(char *)((int)DAT_08001804 + 0x29d) =
         (char)((ushort)*(undefined2 *)((int)DAT_08001804 + 0x29b) >> 8) + 'U' +
         *(char *)((int)DAT_08001804 + 0x29a) + (char)*(undefined2 *)((int)DAT_08001804 + 0x29b);
    *(undefined1 *)((int)puVar3 + 0xe) = 5;
    *puVar3 = puVar3[4];
    uVar4 = FUN_080020da();
    *(undefined2 *)(puVar3 + 2) = uVar4;
    FUN_080020a0((int)puVar3 + 0x29a,*(ushort *)((int)puVar3 + 0x29b) + 4);
  }
  else if (cVar1 == '\x05') {
    iVar5 = FUN_080020c4();
    if (iVar5 == 0) goto LAB_080016de;
    if (iVar5 == 2) {
      FUN_080020f0();
      *(undefined1 *)((int)puVar3 + 0xe) = 0;
    }
  }
  if ((*(byte *)((int)puVar3 + 0xf) & 1) == 0) {
    return;
  }
LAB_080016ec:
  iVar5 = FUN_080020c4();
  if (iVar5 != 2) {
    return;
  }
  FUN_080020f0();
  *(byte *)((int)puVar3 + 0xf) = *(byte *)((int)puVar3 + 0xf) & 0xfe;
  return;
}



/* ===== FUN_08001708 @ 08001708 | callers: FUN_080010aa ===== */

int FUN_08001708(void)

{
  int iVar1;
  byte bVar2;
  
  iVar1 = DAT_08001804;
  bVar2 = *(byte *)(DAT_08001804 + 0xf) & 0x7f;
  if (*(char *)(DAT_08001804 + 0xe) == '\x02') {
    *(undefined1 *)(DAT_08001804 + 0xe) = 3;
    *(byte *)(iVar1 + 0xf) = bVar2;
    return iVar1 + 0x29a;
  }
  if (*(char *)(DAT_08001804 + 0xe) == '\a') {
    *(undefined1 *)(DAT_08001804 + 0xe) = 8;
    *(byte *)(iVar1 + 0xf) = bVar2;
    return iVar1 + 0x29a;
  }
  return 0;
}



/* ===== FUN_08001738 @ 08001738 | callers: FUN_08001286 ===== */

byte FUN_08001738(void)

{
  return *(byte *)(DAT_08001804 + 0xf) >> 7;
}



/* ===== FUN_08001740 @ 08001740 | callers: FUN_080010aa ===== */

bool FUN_08001740(void)

{
  int iVar1;
  
  iVar1 = FUN_0800043e();
  return iVar1 == 4;
}



/* ===== FUN_08001750 @ 08001750 | callers: FUN_080010aa ===== */

undefined4 FUN_08001750(void)

{
  char cVar1;
  
  cVar1 = *(char *)(DAT_08001804 + 0xe);
  if ((cVar1 != '\x01' && cVar1 != '\x02') && (cVar1 != '\x03' && cVar1 != '\x04')) {
    return 0;
  }
  return 1;
}



/* ===== FUN_0800176c @ 0800176c | callers: FUN_080010aa ===== */

void FUN_0800176c(void)

{
  undefined1 uVar1;
  
  if (*(char *)(DAT_08001804 + 0xe) == '\x03') {
    uVar1 = 2;
  }
  else {
    if (*(char *)(DAT_08001804 + 0xe) != '\b') {
      return;
    }
    uVar1 = 7;
  }
  *(undefined1 *)(DAT_08001804 + 0xe) = uVar1;
  return;
}



/* ===== FUN_08001784 @ 08001784 | callers: FUN_0800123a,FUN_080010aa ===== */

void FUN_08001784(void)

{
  undefined1 uVar1;
  
  if (*(char *)(DAT_08001804 + 0xe) == '\x03') {
    uVar1 = 4;
  }
  else {
    if (*(char *)(DAT_08001804 + 0xe) != '\b') {
      return;
    }
    uVar1 = 9;
  }
  *(undefined1 *)(DAT_08001804 + 0xe) = uVar1;
  return;
}



/* ===== FUN_0800179c @ 0800179c | callers: FUN_08001248 ===== */

int FUN_0800179c(uint param_1)

{
  int iVar1;
  int iVar2;
  byte bVar3;
  
  FUN_080014b4();
  FUN_080015ee();
  iVar1 = DAT_08001804;
  if ((*(byte *)(DAT_08001804 + 0xf) & 3) != 0) {
    return 0;
  }
  switch(*(undefined1 *)(DAT_08001804 + 0xe)) {
  default:
    goto switchD_080017b8_caseD_0;
  case 1:
  case 2:
    bVar3 = *(byte *)(DAT_08001804 + 0x20);
    break;
  case 3:
  case 4:
  case 5:
  case 8:
  case 9:
  case 10:
    goto switchD_080017b8_caseD_3;
  case 6:
  case 7:
    bVar3 = *(byte *)(DAT_08001804 + 0x24);
  }
  if (bVar3 < 0x50) {
switchD_080017b8_caseD_0:
    bVar3 = 0;
    if (((param_1 & 1) != 0) && (iVar2 = FUN_0800043e(), iVar2 == 4)) {
      bVar3 = 2;
    }
    if (((param_1 & 2) != 0) && (iVar2 = FUN_0800210c(), iVar2 != 0)) {
      bVar3 = bVar3 | 1;
    }
    if (bVar3 != 0) {
      *(byte *)(iVar1 + 0xf) = *(byte *)(iVar1 + 0xf) | bVar3;
      *(undefined1 *)(iVar1 + 100) = 0xfe;
      *(undefined2 *)(iVar1 + 0x65) = 0x232;
      *(undefined4 *)(iVar1 + 4) = *(undefined4 *)(iVar1 + 0x18);
      return iVar1 + 100;
    }
  }
switchD_080017b8_caseD_3:
  return 0;
}



/* ===== FUN_08001828 @ 08001828 | callers: FUN_0800125a ===== */

byte FUN_08001828(void)

{
  ushort uVar1;
  int iVar2;
  int iVar3;
  byte bVar4;
  int iVar5;
  
  iVar2 = DAT_080019c4;
  bVar4 = *(byte *)(DAT_080019c4 + 0xf);
  if ((bVar4 & 3) != 0) {
    uVar1 = *(ushort *)(DAT_080019c4 + 0x65);
    if (uVar1 == 0) {
      bVar4 = bVar4 & 0xfc;
    }
    else {
      *(char *)(DAT_080019c4 + 0x67) =
           *(char *)(DAT_080019c4 + 100) + (char)uVar1 + (char)(uVar1 >> 8) + 'U';
      iVar5 = uVar1 + 4;
      *(undefined4 *)(iVar2 + 4) = *(undefined4 *)(iVar2 + 0x18);
      if ((bVar4 & 2) != 0) {
        iVar3 = FUN_0800043e();
        if (iVar3 == 4) {
          FUN_0800078e(0x81,iVar2 + 100,iVar5,0x236);
        }
        else {
          bVar4 = bVar4 & 0xfd;
        }
      }
      if ((bVar4 & 1) != 0) {
        iVar3 = FUN_0800210c();
        if (iVar3 == 0) {
          bVar4 = bVar4 & 0xfe;
        }
        else {
          FUN_080020a0(iVar2 + 100,iVar5);
        }
      }
    }
    *(byte *)(iVar2 + 0xf) = bVar4;
  }
  return bVar4 & 3;
}



/* ===== FUN_080018a6 @ 080018a6 | callers: FUN_080011f6 ===== */

void FUN_080018a6(void)

{
  char cVar1;
  int *piVar2;
  undefined2 uVar3;
  uint uVar4;
  int iVar5;
  undefined4 uVar6;
  bool bVar7;
  
  FUN_080014b4();
  FUN_080015ee();
  piVar2 = DAT_080019c4;
  if (*(char *)((int)DAT_080019c4 + 0xe) == '\x01') {
    uVar4 = FUN_080020ea();
    if (uVar4 != *(ushort *)((int)piVar2 + 10)) {
      uVar3 = FUN_080020ea();
      *(undefined2 *)((int)piVar2 + 10) = uVar3;
      iVar5 = piVar2[5];
LAB_08001908:
      *piVar2 = iVar5;
    }
  }
  else if (*(char *)((int)DAT_080019c4 + 0xe) == '\x05') {
    uVar4 = FUN_080020da();
    if (uVar4 != *(ushort *)(piVar2 + 2)) {
      uVar3 = FUN_080020da();
      *(undefined2 *)(piVar2 + 2) = uVar3;
      iVar5 = piVar2[4];
      goto LAB_08001908;
    }
  }
  else if (((*(byte *)((int)DAT_080019c4 + 0xf) & 1) != 0) &&
          (uVar4 = FUN_080020da(), uVar4 != *(ushort *)(piVar2 + 2))) {
    uVar3 = FUN_080020da();
    *(undefined2 *)(piVar2 + 2) = uVar3;
    piVar2[1] = piVar2[6];
  }
  iVar5 = *piVar2;
  *piVar2 = iVar5 + -1;
  if (iVar5 + -1 == 0) {
    cVar1 = *(char *)((int)piVar2 + 0xe);
    if (cVar1 == '\x01') {
      FUN_08002102();
    }
    else if (cVar1 == '\x05') {
      FUN_080020f0();
    }
    else {
      if (cVar1 == '\x06') {
        uVar6 = 2;
      }
      else {
        if (cVar1 != '\n') goto LAB_08001936;
        uVar6 = 0x81;
      }
      FUN_08000862(uVar6);
    }
    *(undefined1 *)((int)piVar2 + 0xe) = 0;
  }
LAB_08001936:
  iVar5 = piVar2[1];
  bVar7 = iVar5 != 0;
  if (bVar7) {
    iVar5 = iVar5 + -1;
  }
  if (bVar7) {
    piVar2[1] = iVar5;
    return;
  }
  if ((*(byte *)((int)piVar2 + 0xf) & 1) != 0) {
    FUN_080020f0();
    *(byte *)((int)piVar2 + 0xf) = *(byte *)((int)piVar2 + 0xf) & 0xfe;
  }
  if ((*(byte *)((int)piVar2 + 0xf) & 2) == 0) {
    return;
  }
  FUN_08000862(0x81);
  *(byte *)((int)piVar2 + 0xf) = *(byte *)((int)piVar2 + 0xf) & 0xfd;
  return;
}



/* ===== FUN_08001976 @ 08001976 | callers: FUN_0800126a ===== */

void FUN_08001976(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  
  iVar1 = DAT_080019c4;
  *(undefined4 *)(DAT_080019c4 + 0x18) = param_3;
  *(undefined4 *)(iVar1 + 0x10) = param_1;
  *(undefined4 *)(iVar1 + 0x14) = param_2;
  return;
}



/* ===== FUN_08001986 @ 08001986 | callers: FUN_08001338 ===== */

void FUN_08001986(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 local_20;
  undefined4 local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  undefined4 local_c [3];
  
  iVar1 = DAT_080019c4;
  local_c[0] = 0;
  *(undefined1 *)(DAT_080019c4 + 0xe) = 0;
  *(undefined1 *)(iVar1 + 0xf) = 0;
  *(undefined4 *)(iVar1 + 0x1c) = 0;
  uVar2 = DAT_080019c8;
  *(undefined4 *)(iVar1 + 0x10) = DAT_080019c8;
  *(undefined4 *)(iVar1 + 0x14) = uVar2;
  *(undefined4 *)(iVar1 + 0x18) = uVar2;
  local_20 = DAT_080019cc;
  local_18 = DAT_080019d0;
  local_14 = DAT_080019d0 + 0x12;
  local_10 = 0x20;
  local_1c = param_1;
  FUN_08000d04(&local_20);
  local_c[0] = DAT_080019d4;
  FUN_0800231c(local_c);
  return;
}



/* ===== FUN_080019d8 @ 080019d8 | callers: FUN_080019f6 ===== */

undefined4 FUN_080019d8(void)

{
  undefined4 uVar1;
  uint uVar2;
  
  uVar1 = 0;
  uVar2 = *(uint *)(DAT_08001a8c + 0xc);
  if ((uVar2 & 1) != 0) {
    return 1;
  }
  if ((int)(uVar2 << 0x1d) < 0) {
    uVar1 = 2;
  }
  else if ((int)(uVar2 << 0x1b) < 0) {
    return 3;
  }
  return uVar1;
}



/* ===== FUN_080019f6 @ 080019f6 | callers: FUN_08001a34 ===== */

void FUN_080019f6(void)

{
  int iVar1;
  int iVar2;
  
  iVar2 = 0xfff;
  while ((iVar1 = FUN_080019d8(), iVar1 == 1 && (iVar2 = iVar2 + -1, iVar2 != 0))) {
    iVar1 = 0xfd;
    do {
      iVar1 = iVar1 + -1;
    } while (iVar1 != 0);
  }
  return;
}



/* ===== FUN_08001a12 @ 08001a12 | callers: FUN_08001ac0,FUN_08000f3e,FUN_08001b1c ===== */

void FUN_08001a12(void)

{
  int iVar1;
  
  iVar1 = DAT_08001a8c;
  *(undefined4 *)(DAT_08001a8c + 4) = DAT_08001a90;
  *(undefined4 *)(iVar1 + 4) = DAT_08001a94;
  return;
}



/* ===== FUN_08001a1e @ 08001a1e | callers: FUN_08001ac0,FUN_08001064,FUN_08000f3e,FUN_08001b1c ===== */

void FUN_08001a1e(void)

{
  *(uint *)(DAT_08001a8c + 0x10) = *(uint *)(DAT_08001a8c + 0x10) | 0x80;
  return;
}



/* ===== FUN_08001a2a @ 08001a2a | callers: FUN_08001b1c ===== */

uint FUN_08001a2a(void)

{
  return (uint)(*(int *)(DAT_08001a8c + 0x10) << 0x18) >> 0x1f;
}



/* ===== FUN_08001a34 @ 08001a34 | callers: FUN_08001a7a,FUN_08001a82 ===== */

void FUN_08001a34(uint param_1,undefined2 *param_2,undefined2 param_3)

{
  int iVar1;
  int iVar2;
  
  iVar2 = FUN_080019f6();
  iVar1 = DAT_08001a8c;
  if (iVar2 != 1) {
    *(uint *)(DAT_08001a8c + 0xc) = *(uint *)(DAT_08001a8c + 0xc) | 0x14;
    *(uint *)(iVar1 + 0x10) = *(uint *)(iVar1 + 0x10) | param_1;
    if (param_1 == 1) {
      *param_2 = param_3;
    }
    else if (param_1 == 2) {
      *(undefined2 **)(iVar1 + 0x14) = param_2;
      *(uint *)(iVar1 + 0x10) = *(uint *)(iVar1 + 0x10) | 0x40;
    }
    iVar2 = FUN_080019f6();
    if (iVar2 != 1) {
      *(uint *)(iVar1 + 0x10) = *(uint *)(iVar1 + 0x10) & ~param_1;
    }
  }
  return;
}



/* ===== FUN_08001a7a @ 08001a7a | callers: FUN_08001ac0,FUN_08000f3e,FUN_08001b1c ===== */

void FUN_08001a7a(undefined4 param_1)

{
  FUN_08001a34(2,param_1,0);
  return;
}



/* ===== FUN_08001a82 @ 08001a82 | callers: FUN_08001ac0,FUN_08001004,FUN_08001b1c ===== */

void FUN_08001a82(undefined4 param_1,undefined4 param_2)

{
  FUN_08001a34(1,param_1,param_2);
  return;
}



/* ===== FUN_08001a98 @ 08001a98 | callers: FUN_080012e4,FUN_080011a8 ===== */

uint FUN_08001a98(undefined4 *param_1,int param_2)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  uint *puVar5;
  uint uVar6;
  undefined4 uVar7;
  
  puVar5 = DAT_08001abc;
  DAT_08001abc[2] = DAT_08001abc[2] | 1;
  for (; param_2 != 0; param_2 = param_2 + -1) {
    uVar7 = *param_1;
    param_1 = param_1 + 1;
    bVar2 = (byte)uVar7;
    bVar3 = (byte)((uint)uVar7 >> 8);
    bVar4 = (byte)((uint)uVar7 >> 0x10);
    bVar1 = (byte)((uint)uVar7 >> 0x18);
    *puVar5 = (uint)(byte)((((((((bVar2 & 1) << 1 | bVar2 >> 1 & 1) << 1 | bVar2 >> 2 & 1) << 1 |
                              bVar2 >> 3 & 1) << 1 | bVar2 >> 4 & 1) << 1 | bVar2 >> 5 & 1) << 1 |
                           bVar2 >> 6 & 1) << 1 | bVar2 >> 7) << 0x18 |
              (uint)(byte)((((((((bVar3 & 1) << 1 | bVar3 >> 1 & 1) << 1 | bVar3 >> 2 & 1) << 1 |
                              bVar3 >> 3 & 1) << 1 | bVar3 >> 4 & 1) << 1 | bVar3 >> 5 & 1) << 1 |
                           bVar3 >> 6 & 1) << 1 | bVar3 >> 7) << 0x10 |
              (uint)(byte)((((((((bVar4 & 1) << 1 | bVar4 >> 1 & 1) << 1 | bVar4 >> 2 & 1) << 1 |
                              bVar4 >> 3 & 1) << 1 | bVar4 >> 4 & 1) << 1 | bVar4 >> 5 & 1) << 1 |
                           bVar4 >> 6 & 1) << 1 | bVar4 >> 7) << 8 |
              (uint)(byte)((((((((bVar1 & 1) << 1 | bVar1 >> 1 & 1) << 1 | bVar1 >> 2 & 1) << 1 |
                              bVar1 >> 3 & 1) << 1 | bVar1 >> 4 & 1) << 1 | bVar1 >> 5 & 1) << 1 |
                           bVar1 >> 6 & 1) << 1 | bVar1 >> 7);
  }
  uVar6 = *puVar5;
  bVar2 = (byte)uVar6;
  bVar3 = (byte)(uVar6 >> 8);
  bVar4 = (byte)(uVar6 >> 0x10);
  bVar1 = (byte)(uVar6 >> 0x18);
  return ~((uint)(byte)((((((((bVar2 & 1) << 1 | bVar2 >> 1 & 1) << 1 | bVar2 >> 2 & 1) << 1 |
                           bVar2 >> 3 & 1) << 1 | bVar2 >> 4 & 1) << 1 | bVar2 >> 5 & 1) << 1 |
                        bVar2 >> 6 & 1) << 1 | bVar2 >> 7) << 0x18 |
           (uint)(byte)((((((((bVar3 & 1) << 1 | bVar3 >> 1 & 1) << 1 | bVar3 >> 2 & 1) << 1 |
                           bVar3 >> 3 & 1) << 1 | bVar3 >> 4 & 1) << 1 | bVar3 >> 5 & 1) << 1 |
                        bVar3 >> 6 & 1) << 1 | bVar3 >> 7) << 0x10 |
           (uint)(byte)((((((((bVar4 & 1) << 1 | bVar4 >> 1 & 1) << 1 | bVar4 >> 2 & 1) << 1 |
                           bVar4 >> 3 & 1) << 1 | bVar4 >> 4 & 1) << 1 | bVar4 >> 5 & 1) << 1 |
                        bVar4 >> 6 & 1) << 1 | bVar4 >> 7) << 8 |
          (uint)(byte)((((((((bVar1 & 1) << 1 | bVar1 >> 1 & 1) << 1 | bVar1 >> 2 & 1) << 1 |
                          bVar1 >> 3 & 1) << 1 | bVar1 >> 4 & 1) << 1 | bVar1 >> 5 & 1) << 1 |
                       bVar1 >> 6 & 1) << 1 | bVar1 >> 7));
}



/* ===== FUN_08001ac0 @ 08001ac0 | callers: FUN_08001338 ===== */

undefined4 FUN_08001ac0(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  FUN_08001a12();
  if ((*(short *)(DAT_08001bd8 + 0x7fe) != 0x5aa5) && (*(short *)(DAT_08001bd8 + 0xffe) != 0x5aa5))
  {
    FUN_08001a7a(DAT_08001bd8);
    uVar1 = FUN_08001a82(DAT_08001bdc,0x5aa5);
  }
  FUN_08001a1e();
  return uVar1;
}



/* ===== FUN_08001af6 @ 08001af6 | callers: FUN_08001298,FUN_08000ebe ===== */

undefined2 FUN_08001af6(uint param_1)

{
  int iVar1;
  
  if (0x3fe < param_1) {
    return 0xffff;
  }
  iVar1 = DAT_08001bd8;
  if (*(short *)(DAT_08001bd8 + 0x7fe) != 0x5aa5) {
    iVar1 = DAT_08001bd8 + 0x800;
  }
  return *(undefined2 *)(iVar1 + param_1 * 2);
}



/* ===== FUN_08001b1c @ 08001b1c | callers: FUN_08000ebe,FUN_080012a8 ===== */

int FUN_08001b1c(uint param_1,uint param_2)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  
  iVar4 = DAT_08001bd8;
  iVar1 = FUN_08001a2a();
  if (param_1 < 0x3ff) {
    if (*(short *)(iVar4 + 0x7fe) != 0x5aa5) {
      iVar4 = iVar4 + 0x800;
    }
    FUN_08001a12();
    if (*(short *)(iVar4 + param_1 * 2) == -1) {
      iVar6 = FUN_08001a82(iVar4 + param_1 * 2,param_2);
    }
    else {
      if (iVar4 == DAT_08001bd8) {
        iVar5 = iVar4 + 0x800;
      }
      else {
        iVar5 = iVar4 + -0x800;
      }
      uVar2 = 0;
      do {
        if (*(short *)(iVar5 + uVar2 * 2) != -1) {
          FUN_08001a7a(iVar5);
          break;
        }
        uVar2 = uVar2 + 1;
      } while (uVar2 < 0x400);
      uVar2 = 0;
      do {
        uVar3 = param_2;
        if (uVar2 != param_1) {
          uVar3 = (uint)*(ushort *)(iVar4 + uVar2 * 2);
        }
        iVar6 = FUN_08001a82(iVar5 + uVar2 * 2,uVar3);
        if (iVar6 != 0) goto LAB_08001bc6;
        uVar2 = uVar2 + 1;
      } while (uVar2 < 0x3ff);
      iVar6 = FUN_08001a82(iVar5 + 0x7fe,0x5aa5);
      if (iVar6 == 0) {
        iVar6 = FUN_08001a7a(iVar4);
      }
    }
  }
  else {
    iVar6 = 2;
  }
LAB_08001bc6:
  if (iVar1 != 0) {
    FUN_08001a1e();
  }
  return iVar6;
}



/* ===== FUN_08001c24 @ 08001c24 | callers: FUN_0800221a,FUN_08002146 ===== */

int FUN_08001c24(int param_1,uint param_2)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  
  iVar2 = DAT_08001efc;
  iVar1 = DAT_08001ef0;
  uVar5 = param_2;
  if (*(int *)(DAT_08001ef0 + 8) != 0) {
    return 0;
  }
  for (; uVar5 != 0; uVar5 = uVar5 - uVar4) {
    uVar4 = 0x40 - *(int *)(iVar2 + 0x70);
    uVar3 = *(uint *)(iVar1 + 0xc);
    if (uVar4 < uVar3) {
      uVar4 = -uVar3 + 0x40;
    }
    else {
      uVar4 = -uVar3 + uVar4;
    }
    if (uVar5 < uVar4) {
      uVar4 = uVar5;
    }
    if (uVar4 == 0) break;
    FUN_08002618(param_1,iVar1 + uVar3 + 0x10,uVar4);
    param_1 = param_1 + uVar4;
    *(uint *)(iVar1 + 0xc) = *(int *)(iVar1 + 0xc) + uVar4 & 0x3f;
  }
  if (((*DAT_08001f04 & 2) != 0) &&
     (((-*(int *)(iVar1 + 0xc) - *(int *)(iVar2 + 0x70)) + 0x80U & 0x3f) < 0x30)) {
    *DAT_08001ef4 = 0x20000;
  }
  return param_2 - uVar5;
}



/* ===== FUN_08001cb2 @ 08001cb2 | callers: FUN_0800221a,FUN_08002146 ===== */

uint FUN_08001cb2(undefined4 param_1,uint param_2)

{
  int iVar1;
  uint uVar2;
  
  iVar1 = DAT_08001efc;
  if ((DAT_08001ef0[2] == 0) && (param_2 != 0)) {
    uVar2 = *(uint *)(DAT_08001efc + 0x80);
    if ((uVar2 & 1) == 0) {
      if (0xffff < param_2) {
        param_2 = 0xffff;
      }
      *DAT_08001ef0 = param_2;
      *(undefined4 *)(iVar1 + 0x8c) = param_1;
      *(uint *)(iVar1 + 0x84) = param_2;
      *(uint *)(iVar1 + 0x80) = uVar2 | 1;
      return param_2;
    }
  }
  return 0;
}



/* ===== FUN_08001cf8 @ 08001cf8 | callers: FUN_0800221a,FUN_080020da ===== */

int FUN_08001cf8(void)

{
  if (*DAT_08001ef0 == 0) {
    return 0;
  }
  return *DAT_08001ef0 - *(int *)(DAT_08001efc + 0x84);
}



/* ===== FUN_08001d0c @ 08001d0c | callers: FUN_0800221a,FUN_0800231c,FUN_08002038,FUN_08002146,FUN_080020f0 ===== */

void FUN_08001d0c(void)

{
  uint uVar1;
  bool bVar2;
  
  uVar1 = *(uint *)(DAT_08001efc + 0x80);
  bVar2 = (uVar1 & 1) != 0;
  if (bVar2) {
    uVar1 = uVar1 & 0xfffffffe;
  }
  if (bVar2) {
    *(uint *)(DAT_08001efc + 0x80) = uVar1;
  }
  *DAT_08001ef0 = 0;
  return;
}



/* ===== FUN_08001d28 @ 08001d28 | callers: FUN_08002146 ===== */

uint FUN_08001d28(void)

{
  return ~*(uint *)(DAT_08001efc + 0x80) & 1;
}



/* ===== FUN_08001d36 @ 08001d36 | callers: FUN_0800221a,FUN_08002146 ===== */

undefined4 FUN_08001d36(void)

{
  return *(undefined4 *)(DAT_08001ef0 + 8);
}



/* ===== FUN_08001d3c @ 08001d3c | callers: FUN_0800221a,FUN_08002146 ===== */

void FUN_08001d3c(void)

{
  int iVar1;
  int iVar2;
  
  iVar2 = DAT_08001efc;
  iVar1 = DAT_08001ef0;
  if (*(int *)(DAT_08001ef0 + 8) != 0) {
    *(undefined4 *)(DAT_08001efc + 0x70) = 0x40;
    *(uint *)(iVar2 + 0x6c) = *(uint *)(iVar2 + 0x6c) | 1;
    *(undefined4 *)(iVar1 + 0xc) = 0;
    *DAT_08001ef8 = *DAT_08001ef8 | 0xc0;
    *(undefined4 *)(iVar1 + 8) = 0;
    *DAT_08001ef4 = 0x20000;
    return;
  }
  return;
}



/* ===== FUN_08001dc6 @ 08001dc6 | callers: FUN_0800231c,FUN_0800211a ===== */

void FUN_08001dc6(int *param_1)

{
  undefined4 *puVar1;
  undefined2 *puVar2;
  int iVar3;
  undefined4 uVar4;
  int iVar5;
  undefined2 uVar6;
  uint uVar7;
  uint uVar8;
  undefined1 auStack_38 [8];
  int local_30;
  
  iVar5 = DAT_08001f08;
  *(undefined4 *)(DAT_08001f08 + 0x180) = 0x40;
  DataSynchronizationBarrier(0xf);
  InstructionSynchronizationBarrier(0xf);
  *(undefined4 *)(iVar5 + 0x17c) = 0x10000;
  DataSynchronizationBarrier(0xf);
  InstructionSynchronizationBarrier(0xf);
  *(undefined4 *)(iVar5 + 0x17c) = 0x20000;
  DataSynchronizationBarrier(0xf);
  InstructionSynchronizationBarrier(0xf);
  FUN_0800264a(DAT_08001ef0,0x50);
  FUN_08001f24(0x20000);
  FUN_08001f36(0x20000);
  FUN_08001f24(0x20000,0);
  iVar3 = DAT_08001efc;
  puVar1 = (undefined4 *)(DAT_08001efc + 0x6c);
  *puVar1 = 0;
  uVar4 = DAT_08001f00;
  *(undefined4 *)(iVar3 + 0x74) = DAT_08001f00;
  *(undefined4 *)(iVar3 + 0x78) = DAT_08001f0c;
  *(undefined4 *)(iVar3 + 0x70) = 0x40;
  *puVar1 = 0x21a7;
  *(undefined4 *)(iVar3 + 0x80) = 0;
  *(undefined4 *)(iVar3 + 0x88) = uVar4;
  *(undefined4 *)(iVar3 + 0x80) = 0x1192;
  *(undefined4 *)(iVar3 + 4) = 0x1100000;
  FUN_08001f48(auStack_38);
  uVar7 = (uint)(local_30 * 0x19) / (uint)(*param_1 << 2);
  uVar8 = (uint)((ulonglong)DAT_08001f10 * (ulonglong)uVar7 >> 0x25);
  *DAT_08001f14 =
       (ushort)((uint)((int)((ulonglong)DAT_08001f10 *
                             (ulonglong)((uVar7 + uVar8 * -100) * 0x10 + 0x32) >> 0x20) << 0x17) >>
               0x1c) | (ushort)(uVar8 << 4);
  puVar2 = DAT_08001ef8;
  uVar6 = 0xc1;
  if (param_1[1] != 0) {
    uVar6 = 0x2c1;
  }
  *DAT_08001ef8 = uVar6;
  puVar2[-2] = 0;
  *DAT_08001eec = 0;
  *DAT_08001f18 = 0x200c;
  *(undefined1 *)(DAT_08001f1c + 0x400) = 0xa0;
  iVar3 = DAT_08001f20;
  *(undefined1 *)(DAT_08001f20 + 0x400) = 0xa0;
  *(undefined1 *)(iVar3 + 0x401) = 0xa0;
  *(undefined4 *)(iVar5 + 0x280) = 0x40;
  *(undefined4 *)(iVar5 + 0x27c) = 0x10000;
  *(undefined4 *)(iVar5 + 0x27c) = 0x20000;
  *(undefined4 *)(iVar5 + 0x100) = 0x40;
  *(undefined4 *)(iVar5 + 0xfc) = 0x10000;
  *(undefined4 *)(iVar5 + 0xfc) = 0x20000;
  *DAT_08001ef4 = 0x20000;
  return;
}



/* ===== FUN_08001f24 @ 08001f24 | callers: FUN_08001dc6 ===== */

void FUN_08001f24(uint param_1,int param_2)

{
  if (param_2 == 0) {
    param_1 = *(uint *)(DAT_08002014 + 0x10) & ~param_1;
  }
  else {
    param_1 = *(uint *)(DAT_08002014 + 0x10) | param_1;
  }
  *(uint *)(DAT_08002014 + 0x10) = param_1;
  return;
}



/* ===== FUN_08001f36 @ 08001f36 | callers: FUN_08001dc6 ===== */

void FUN_08001f36(uint param_1,int param_2)

{
  if (param_2 == 0) {
    param_1 = *(uint *)(DAT_08002014 + 0x1c) & ~param_1;
  }
  else {
    param_1 = *(uint *)(DAT_08002014 + 0x1c) | param_1;
  }
  *(uint *)(DAT_08002014 + 0x1c) = param_1;
  return;
}



/* ===== FUN_08001f48 @ 08001f48 | callers: FUN_08001dc6 ===== */

void FUN_08001f48(uint *param_1)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  undefined4 local_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined4 local_18;
  
  iVar1 = DAT_08002014;
  local_28 = DAT_08002018;
  uStack_24 = DAT_0800201c;
  uStack_20 = DAT_08002020;
  uStack_1c = DAT_08002024;
  local_18 = DAT_08002028;
  uVar4 = *(uint *)(DAT_08002014 + 4) & 0xc;
  uVar3 = DAT_0800202c;
  if (uVar4 != 0) {
    if (uVar4 == 4) {
      *param_1 = DAT_08002030;
      goto LAB_08001fc4;
    }
    if (uVar4 == 8) {
      uVar3 = *(uint *)(DAT_08002014 + 4) >> 0x12 & 0xf;
      if (uVar3 == 0xd) {
        iVar2 = 6;
      }
      else {
        iVar2 = uVar3 + 2;
      }
      if ((*(uint *)(DAT_08002014 + 4) & 0x10000) != 0) {
        uVar3 = DAT_08002030;
        if ((*(uint *)(DAT_08002014 + 0x2c) & 0x10000) != 0) {
          uVar3 = (((uint)(*(int *)(DAT_08002014 + 0x2c) << 0x14) >> 0x1c) + 2) *
                  (DAT_08002030 / (((uint)(*(int *)(DAT_08002014 + 0x2c) << 0x18) >> 0x1c) + 1));
        }
        *param_1 = iVar2 * (uVar3 / ((*(uint *)(DAT_08002014 + 0x2c) & 0xf) + 1));
        goto LAB_08001fc4;
      }
      uVar3 = DAT_08002034 * iVar2;
    }
  }
  *param_1 = uVar3;
LAB_08001fc4:
  uVar3 = *param_1 >> *(sbyte *)((int)&local_28 + (*(uint *)(iVar1 + 4) >> 4 & 0xf));
  param_1[1] = uVar3;
  param_1[2] = uVar3 >> *(sbyte *)((int)&local_28 + (*(uint *)(iVar1 + 4) >> 8 & 7));
  uVar3 = uVar3 >> *(sbyte *)((int)&local_28 + (*(uint *)(iVar1 + 4) >> 0xb & 7));
  param_1[3] = uVar3;
  param_1[4] = uVar3 / *(byte *)((int)&local_18 + (*(uint *)(iVar1 + 4) >> 0xe & 3));
  return;
}



/* ===== FUN_08002038 @ 08002038 | callers: FUN_0800221a,FUN_0800211a ===== */

void FUN_08002038(uint param_1)

{
  byte bVar1;
  int *piVar2;
  undefined4 uVar3;
  
  piVar2 = DAT_08002388;
  bVar1 = *(byte *)((int)DAT_08002388 + 0x16);
  *(char *)((int)DAT_08002388 + 0x16) = (char)param_1;
  if (param_1 != 1) {
    *(undefined1 *)((int)piVar2 + 0x17) = 0;
  }
  FUN_08001d0c();
  *(undefined2 *)((int)piVar2 + 0x12) = 0;
  *(undefined2 *)(piVar2 + 5) = 0;
  *(undefined2 *)(piVar2 + 3) = 0;
  *(undefined2 *)((int)piVar2 + 0xe) = 0;
  *(undefined2 *)(piVar2 + 4) = 0;
  if (bVar1 == param_1) {
    return;
  }
  if (bVar1 == 2) {
    if (*piVar2 == 0) {
      return;
    }
    if (param_1 != 2) {
      uVar3 = 0;
      goto LAB_08002088;
    }
  }
  else {
    if (param_1 != 2) {
      return;
    }
    if (*piVar2 == 0) {
      return;
    }
  }
  uVar3 = 1;
LAB_08002088:
                    /* WARNING: Could not recover jumptable at 0x0800208e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)*piVar2)(uVar3);
  return;
}



/* ===== FUN_08002094 @ 08002094 | callers: FUN_080015ee ===== */

void FUN_08002094(undefined4 param_1,undefined2 param_2)

{
  int iVar1;
  
  iVar1 = DAT_08002388;
  *(undefined4 *)(DAT_08002388 + 8) = param_1;
  *(undefined2 *)(iVar1 + 0x12) = param_2;
  *(undefined2 *)(iVar1 + 0x14) = 0;
  return;
}



/* ===== FUN_080020a0 @ 080020a0 | callers: FUN_080015ee,FUN_08001828 ===== */

void FUN_080020a0(undefined4 param_1,undefined2 param_2)

{
  int iVar1;
  
  iVar1 = DAT_08002388;
  *(undefined4 *)(DAT_08002388 + 4) = param_1;
  *(undefined2 *)(iVar1 + 0xc) = param_2;
  *(undefined2 *)(iVar1 + 0xe) = 0;
  *(undefined2 *)(iVar1 + 0x10) = 0;
  return;
}



/* ===== FUN_080020ae @ 080020ae | callers: FUN_080015ee ===== */

undefined4 FUN_080020ae(void)

{
  undefined4 uVar1;
  
  if (*(ushort *)(DAT_08002388 + 0x12) != 0) {
    if (*(ushort *)(DAT_08002388 + 0x14) < *(ushort *)(DAT_08002388 + 0x12)) {
      uVar1 = 1;
    }
    else {
      uVar1 = 2;
    }
    return uVar1;
  }
  return 0;
}



/* ===== FUN_080020c4 @ 080020c4 | callers: FUN_080015ee ===== */

undefined4 FUN_080020c4(void)

{
  undefined4 uVar1;
  
  if (*(ushort *)(DAT_08002388 + 0xc) != 0) {
    if (*(ushort *)(DAT_08002388 + 0xe) < *(ushort *)(DAT_08002388 + 0xc)) {
      uVar1 = 1;
    }
    else {
      uVar1 = 2;
    }
    return uVar1;
  }
  return 0;
}



/* ===== FUN_080020da @ 080020da | callers: FUN_080015ee,FUN_080018a6 ===== */

void FUN_080020da(void)

{
  if ((uint)*(ushort *)(DAT_08002388 + 0xe) + (uint)*(ushort *)(DAT_08002388 + 0x10) == 0) {
    return;
  }
  FUN_08001cf8();
  return;
}



/* ===== FUN_080020ea @ 080020ea | callers: FUN_080015ee,FUN_080018a6 ===== */

undefined2 FUN_080020ea(void)

{
  return *(undefined2 *)(DAT_08002388 + 0x14);
}



/* ===== FUN_080020f0 @ 080020f0 | callers: FUN_080015ee,FUN_080018a6 ===== */

void FUN_080020f0(void)

{
  int iVar1;
  
  FUN_08001d0c();
  iVar1 = DAT_08002388;
  *(undefined2 *)(DAT_08002388 + 0xc) = 0;
  *(undefined2 *)(iVar1 + 0xe) = 0;
  *(undefined2 *)(iVar1 + 0x10) = 0;
  return;
}



/* ===== FUN_08002102 @ 08002102 | callers: FUN_080015ee,FUN_080018a6 ===== */

void FUN_08002102(void)

{
  int iVar1;
  
  iVar1 = DAT_08002388;
  *(undefined2 *)(DAT_08002388 + 0x12) = 0;
  *(undefined2 *)(iVar1 + 0x14) = 0;
  return;
}



/* ===== FUN_0800210c @ 0800210c | callers: FUN_08001408,FUN_080015ee,FUN_0800179c,FUN_0800145a,FUN_08001828 ===== */

bool FUN_0800210c(void)

{
  return *(char *)(DAT_08002388 + 0x16) == '\x02';
}



/* ===== FUN_0800211a @ 0800211a | callers: FUN_08001362 ===== */

void FUN_0800211a(int param_1,undefined4 param_2,int param_3)

{
  undefined4 uVar1;
  undefined4 local_10;
  uint local_c;
  
  local_c = (uint)(param_3 != 0);
  if (param_3 == 0) {
    local_c = 0;
  }
  local_10 = param_2;
  FUN_08001dc6(&local_10);
  if (param_1 == 0) {
    uVar1 = 0;
  }
  else {
    uVar1 = 3;
  }
  FUN_08002038(uVar1);
  return;
}



/* ===== FUN_08002146 @ 08002146 | callers: FUN_08001362 ===== */

undefined4
FUN_08002146(int param_1,int param_2,int param_3,int *param_4,ushort *param_5,int param_6,
            int param_7,int param_8,int *param_9)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  bool bVar5;
  byte local_50 [16];
  undefined4 local_40;
  int iStack_34;
  int iStack_30;
  int iStack_2c;
  int *local_28;
  
  local_40 = 1;
  iVar4 = 0;
  iVar3 = 0;
  local_28 = param_4;
  if (*(char *)(DAT_08002388 + 0x16) == '\x03') {
    iStack_34 = param_1;
    iStack_30 = param_2;
    iStack_2c = param_3;
    if (param_2 != 0) {
      do {
        iVar1 = FUN_08001cb2(param_1,param_2);
        param_1 = param_1 + iVar1;
        param_2 = param_2 - iVar1;
        for (; (iVar2 = FUN_08001d28(), iVar2 == 0 && (param_3 != 0)); param_3 = param_3 + -1) {
          iVar2 = 0x13fd;
          do {
            bVar5 = iVar2 != 0;
            iVar2 = iVar2 + -1;
          } while (bVar5);
        }
        iVar2 = FUN_08001d28();
        if (iVar2 != 0) {
          iVar4 = iVar4 + iVar1;
        }
      } while ((iVar2 != 0 || param_3 != 0) && param_2 != 0);
    }
    FUN_08001d0c();
    if (param_6 != 0) {
      do {
        iVar1 = FUN_08001c24(local_50,1);
        if (iVar1 == 0) {
          iVar1 = FUN_08001d36();
          if (iVar1 == 0) {
            if (param_7 == 0) break;
            iVar1 = 0x13fd;
            do {
              bVar5 = iVar1 != 0;
              iVar1 = iVar1 + -1;
            } while (bVar5);
            param_7 = param_7 + -1;
          }
          else {
            *param_5 = 0x8000;
            param_6 = param_6 + -1;
            iVar3 = iVar3 + 1;
            FUN_08001d3c();
            param_7 = param_8;
            param_5 = param_5 + 1;
          }
        }
        else {
          *param_5 = (ushort)local_50[0];
          param_6 = param_6 + -1;
          iVar3 = iVar3 + 1;
          param_7 = param_8;
          param_5 = param_5 + 1;
        }
      } while (param_6 != 0);
    }
  }
  else {
    local_40 = 0;
  }
  *local_28 = iVar4;
  *param_9 = iVar3;
  return local_40;
}



/* ===== FUN_0800221a @ 0800221a | callers: FUN_080015ee ===== */

void FUN_0800221a(void)

{
  bool bVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  uint in_r3;
  int iVar7;
  int iVar8;
  bool bVar9;
  uint local_20;
  
  iVar6 = DAT_08002388;
  iVar7 = 4;
  iVar8 = DAT_08002388 + 0x18;
  local_20 = in_r3;
  do {
    if (*(char *)(iVar6 + 0x16) == '\x03') {
      return;
    }
    iVar4 = FUN_08001d36();
    bVar1 = iVar4 != 0;
    if (bVar1) {
      FUN_08002038(0);
      FUN_08001d0c();
      FUN_08001d3c();
    }
    if (*(char *)(iVar6 + 0x16) == '\0') {
      iVar4 = FUN_08001c24(&local_20,1);
      if (iVar4 != 0) {
        if (((local_20 & 0xff) != 10 && (local_20 & 0xff) != 3) ||
           ((*(byte *)(iVar6 + 0x17) < 0xd && (iVar4 = FUN_0800235c(&DAT_0800238c), iVar4 != 0)))) {
          if (*(byte *)(iVar6 + 0x17) < 0x28) {
            *(undefined1 *)((uint)*(byte *)(iVar6 + 0x17) + iVar8) = (undefined1)local_20;
            *(char *)(iVar6 + 0x17) = *(char *)(iVar6 + 0x17) + '\x01';
          }
          goto LAB_080022e0;
        }
        FUN_08002038(1);
      }
LAB_080022de:
      if (!bVar1) break;
    }
    else {
      if (*(char *)(iVar6 + 0x16) != '\x02') goto LAB_080022de;
      uVar5 = (uint)*(ushort *)(iVar6 + 0x14);
      bVar9 = *(ushort *)(iVar6 + 0x12) != uVar5;
      if (bVar9) {
        sVar2 = FUN_08001c24(uVar5 + *(int *)(iVar6 + 8));
        *(short *)(iVar6 + 0x14) = sVar2 + *(short *)(iVar6 + 0x14);
      }
      bVar1 = bVar9 || bVar1;
      if ((uint)*(ushort *)(iVar6 + 0xc) == (uint)*(ushort *)(iVar6 + 0xe)) goto LAB_080022de;
      if (*(short *)(iVar6 + 0x10) == 0) {
        uVar3 = FUN_08001cb2((uint)*(ushort *)(iVar6 + 0xe) + *(int *)(iVar6 + 4));
        *(undefined2 *)(iVar6 + 0x10) = uVar3;
      }
      else {
        uVar5 = FUN_08001cf8();
        if (uVar5 == *(ushort *)(iVar6 + 0x10)) {
          *(ushort *)(iVar6 + 0xe) = *(short *)(iVar6 + 0xe) + *(ushort *)(iVar6 + 0x10);
          *(undefined2 *)(iVar6 + 0x10) = 0;
        }
      }
    }
LAB_080022e0:
    iVar7 = iVar7 + -1;
  } while (iVar7 != 0);
  if (*(char *)(iVar6 + 0x16) != '\x01') {
    return;
  }
  iVar7 = FUN_0800235c(&DAT_0800238c);
  if ((((iVar7 == 0) || (*(char *)(iVar6 + 0x17) != '\r')) &&
      (iVar6 = FUN_0800235c(s_AT_AB__BypassMode__08002394), iVar6 == 0)) &&
     (iVar6 = FUN_0800235c(s_AT_AB__BypassModeBLE__080023a8), iVar6 == 0)) {
    FUN_08002038(0);
    return;
  }
  FUN_08002038(2);
  return;
}



/* ===== FUN_0800231c @ 0800231c | callers: FUN_08001986 ===== */

void FUN_0800231c(undefined4 *param_1)

{
  undefined4 *puVar1;
  int iVar2;
  bool bVar3;
  undefined4 local_18;
  undefined4 local_14;
  
  puVar1 = DAT_08002388;
  local_18 = 0;
  local_14 = 0;
  *(undefined1 *)((int)DAT_08002388 + 0x16) = 0;
  *(undefined1 *)((int)puVar1 + 0x17) = 0;
  *puVar1 = *param_1;
  *(undefined2 *)((int)puVar1 + 0x12) = 0;
  *(undefined2 *)(puVar1 + 5) = 0;
  FUN_08001d0c();
  *(undefined2 *)(puVar1 + 3) = 0;
  *(undefined2 *)((int)puVar1 + 0xe) = 0;
  *(undefined2 *)(puVar1 + 4) = 0;
  local_18 = 0xe1000;
  local_14 = 1;
  FUN_08001dc6(&local_18);
  iVar2 = 0x13ff;
  do {
    bVar3 = iVar2 != 0;
    iVar2 = iVar2 + -1;
  } while (bVar3);
  return;
}



/* ===== FUN_0800235c @ 0800235c | callers: FUN_0800221a ===== */

undefined4 FUN_0800235c(char *param_1)

{
  char cVar1;
  char *pcVar2;
  uint uVar3;
  
  cVar1 = *param_1;
  pcVar2 = (char *)(DAT_08002388 + 0x18);
  uVar3 = (uint)*(byte *)(DAT_08002388 + 0x17);
  while( true ) {
    if (cVar1 == '\0') {
      return 1;
    }
    if ((uVar3 == 0) || (cVar1 != *pcVar2)) break;
    param_1 = param_1 + 1;
    cVar1 = *param_1;
    pcVar2 = pcVar2 + 1;
    uVar3 = uVar3 - 1;
  }
  return 0;
}



/* ===== FUN_080023da @ 080023da | callers: FUN_08001338 ===== */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_080023da(void)

{
  undefined4 *puVar1;
  uint *puVar2;
  undefined2 *puVar3;
  undefined4 *puVar4;
  int iVar5;
  uint uVar6;
  
  *DAT_080025ac = *DAT_080025ac & 0xfffffffe;
  puVar2 = DAT_080025b0;
  *DAT_080025b0 = *DAT_080025b0 & 0xfffffffe;
  _DAT_e000e180 = 0x40000;
  DataSynchronizationBarrier(0xf);
  InstructionSynchronizationBarrier(0xf);
  *(undefined1 *)(DAT_080025b4 + 0x400) = 0x30;
  _DAT_e000e280 = 0x40000;
  *DAT_080025b8 = 0x1000000;
  *DAT_080025bc = *DAT_080025bc & 0xfffffff0 | 3;
  *DAT_080025c0 = 0x100;
  *DAT_080025c4 = 0;
  puVar3 = DAT_080025c8;
  *DAT_080025c8 = 1;
  puVar3[-2] = 0x100;
  *DAT_080025cc = 0;
  *DAT_080025d0 = 0;
  puVar3 = DAT_080025d4;
  *DAT_080025d4 = 0x60;
  puVar3[2] = 0x6060;
  puVar3[4] = 0x1401;
  *DAT_080025d8 = 0;
  *DAT_080025dc = 0x4000;
  *DAT_080025e0 = 0x81;
  *DAT_080025bc = *DAT_080025bc & 0xfffffff0 | 0xb;
  *(uint *)(DAT_080025e4 + 4) = *(uint *)(DAT_080025e4 + 4) & 0xffffff3f | 0x40;
  *DAT_080025e8 = *DAT_080025e8 & 0xffffff0f | 0xb0;
  *DAT_080025ec = 0;
  puVar2[1] = 0;
  *DAT_080025f0 = 0;
  *DAT_080025f4 = 0;
  *DAT_080025f8 = *DAT_080025f8 & 0xffc00000 | 0x162800;
  *DAT_080025fc = *DAT_080025fc & 0xffc00000 | 0x15ac00;
  puVar1 = DAT_080025a0;
  uVar6 = DAT_080025a0[2];
  DAT_080025a0[2] = uVar6 | 1;
  iVar5 = 0xd;
  do {
    iVar5 = iVar5 + -1;
  } while (0 < iVar5);
  puVar1[2] = uVar6 | 5;
  do {
  } while ((puVar1[2] & 8) != 0);
  puVar1[2] = puVar1[2] | 4;
  do {
  } while ((puVar1[2] & 4) != 0);
  puVar1[2] = uVar6;
  puVar4 = DAT_08002600;
  uVar6 = DAT_08002600[2];
  DAT_08002600[2] = uVar6 | 1;
  iVar5 = 0xd;
  do {
    iVar5 = iVar5 + -1;
  } while (0 < iVar5);
  puVar4[2] = uVar6 | 5;
  do {
  } while ((puVar4[2] & 8) != 0);
  puVar4[2] = puVar4[2] | 4;
  do {
  } while ((puVar4[2] & 4) != 0);
  puVar4[2] = uVar6;
  *puVar1 = 0;
  *puVar4 = 0;
  puVar1 = DAT_08002608;
  *DAT_08002608 = DAT_08002604;
  *DAT_0800260c = 0x100;
  *puVar2 = 0xf001;
  puVar1[1] = DAT_08002610;
  _DAT_e000e100 = 0x40000;
  return;
}



/* ===== FUN_0800256a @ 0800256a | callers: FUN_08000218 ===== */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0800256a(void)

{
  undefined2 *puVar1;
  
  puVar1 = DAT_080025c4;
  _DAT_e000e180 = 0x40000;
  DataSynchronizationBarrier(0xf);
  InstructionSynchronizationBarrier(0xf);
  InstructionSynchronizationBarrier(0xf);
  *DAT_080025c4 = 0;
  *DAT_080025a8 = (short)((int)puVar1 >> 0x16);
  return;
}



/* ===== FUN_08002590 @ 08002590 | callers: FUN_080011f6 ===== */

int FUN_08002590(void)

{
  return ((uint)(DAT_08002614 * *DAT_080025a4) >> 0xc) + 700;
}



/* ===== FUN_08002618 @ 08002618 | callers: FUN_08001c24 ===== */

void FUN_08002618(undefined4 *param_1,undefined4 *param_2,uint param_3)

{
  undefined4 uVar1;
  bool bVar2;
  
  if ((((uint)param_1 | (uint)param_2) & 3) == 0) {
    for (; 3 < param_3; param_3 = param_3 - 4) {
      uVar1 = *param_2;
      param_2 = param_2 + 1;
      *param_1 = uVar1;
      param_1 = param_1 + 1;
    }
  }
  while (bVar2 = param_3 != 0, param_3 = param_3 - 1, bVar2) {
    *(undefined1 *)param_1 = *(undefined1 *)param_2;
    param_1 = (undefined4 *)((int)param_1 + 1);
    param_2 = (undefined4 *)((int)param_2 + 1);
  }
  return;
}



/* ===== FUN_0800263c @ 0800263c | callers: FUN_0800264e,FUN_0800264a ===== */

void FUN_0800263c(undefined1 *param_1,int param_2,undefined1 param_3)

{
  bool bVar1;
  
  while (bVar1 = param_2 != 0, param_2 = param_2 + -1, bVar1) {
    *param_1 = param_3;
    param_1 = param_1 + 1;
  }
  return;
}



/* ===== FUN_0800264a @ 0800264a | callers: FUN_08001dc6 ===== */

void FUN_0800264a(undefined4 param_1,undefined4 param_2)

{
  FUN_0800263c(param_1,param_2,0);
  return;
}



/* ===== FUN_0800264e @ 0800264e | callers:  ===== */

undefined4 FUN_0800264e(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  FUN_0800263c(param_1,param_3,param_2);
  return param_1;
}



/* ===== FUN_08002660 @ 08002660 | callers:  ===== */

void FUN_08002660(undefined4 param_1,undefined4 param_2,int param_3)

{
  byte bVar1;
  undefined4 *puVar2;
  byte *pbVar3;
  byte *pbVar4;
  byte *extraout_r1;
  byte *pbVar5;
  uint uVar6;
  uint uVar7;
  undefined4 *puVar8;
  code *UNRECOVERED_JUMPTABLE;
  
  puVar2 = puRam08002680;
  for (puVar8 = puRam0800267c; puVar8 < puVar2; puVar8 = puVar8 + 4) {
    param_3 = puVar8[2];
    (*(code *)puVar8[3])(*puVar8,puVar8[1]);
  }
  UNRECOVERED_JUMPTABLE = (code *)0x800267d;
  thunk_FUN_08001338();
  pbVar3 = (byte *)0x0;
  pbVar5 = extraout_r1;
  do {
    bVar1 = *pbVar3;
    uVar7 = bVar1 & 0xf;
    pbVar4 = pbVar3 + 1;
    if ((bVar1 & 0xf) == 0) {
      pbVar4 = pbVar3 + 2;
      uVar7 = (uint)pbVar3[1];
    }
    uVar6 = (uint)(bVar1 >> 4);
    pbVar3 = pbVar4;
    if (uVar6 == 0) {
      uVar6 = (uint)*pbVar4;
      pbVar3 = pbVar4 + 1;
    }
    while (uVar7 = uVar7 - 1, uVar7 != 0) {
      *pbVar5 = *pbVar3;
      pbVar3 = pbVar3 + 1;
      pbVar5 = pbVar5 + 1;
    }
    while (uVar6 = uVar6 - 1, uVar6 != 0) {
      *pbVar5 = 0;
      pbVar5 = pbVar5 + 1;
    }
  } while (pbVar5 < extraout_r1 + param_3);
                    /* WARNING: Could not recover jumptable at 0x080026bc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(0);
  return;
}



/* ===== FUN_080026c0 @ 080026c0 | callers: FUN_08000fb0 ===== */

uint FUN_080026c0(uint param_1,uint param_2)

{
  return param_1 >> (param_2 & 0x1f) | param_1 << 0x20 - (param_2 & 0x1f);
}



/* ===== FUN_080026c8 @ 080026c8 | callers: FUN_0800055e,FUN_080009e6,FUN_0800078e,FUN_08000862,FUN_08000954 ===== */

int FUN_080026c8(uint param_1)

{
  if ((param_1 & 0x80) != 0) {
    return (param_1 & 0x7f) * 0x20 + 0x900 + *DAT_080026f0;
  }
  return param_1 * 0x20 + 0xb00 + *DAT_080026f0;
}



/* ===== FUN_08002702 @ 08002702 | callers: FUN_08002660 ===== */

void FUN_08002702(void)

{
  return;
}



