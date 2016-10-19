import numpy as np
import pyfits
from astropy.table import Table
import pandas as pd
import matplotlib.pyplot as plt

# load TGAS star indices
hdulist = pyfits.open("pairindices_cp01.fits")
t = hdulist[1].data
m1 = t["star1"]
m2 = t["star2"]

# load full TGAS
hdulist_tgas = pyfits.open("stacked_tgas.fits")
table = Table.read('stacked_tgas.fits')
stacked_tgas_df = table.to_pandas()

# get binaries in TGAS
star1_df = stacked_tgas_df.iloc[m1]
star2_df = stacked_tgas_df.iloc[m2]

keep_track = np.vstack((star1_df.source_id, star2_df.source_id)).T

# load kepler-tgas xmatch
kplr_tgas = pd.read_csv("kic_tgas_mod.csv")
epic_tgas = pd.read_csv("epic_tgas_mod.csv")

# find the indices of the star1s and 2s that are in kepler-tgas
m_tgas = star1_df.source_id.isin(kplr_tgas.source_id).values * \
    star2_df.source_id.isin(kplr_tgas.source_id).values
star1_tgas = star1_df.iloc[np.where(m_tgas)[0]]
star2_tgas = star2_df.iloc[np.where(m_tgas)[0]]
print(len(np.where(m_tgas)[0]), "pairs found in kepler")

print(len(star1_tgas.source_id))
print(len(np.unique(star1_tgas.source_id.values)))
print(len(star2_tgas.source_id))
print(len(np.unique(star2_tgas.source_id.values)))

# find the indices of the star1s and 2s that are in epic-tgas
m_tgas_epic = star1_df.source_id.isin(epic_tgas.source_id).values * \
    star2_df.source_id.isin(epic_tgas.source_id).values
star1_tgas_epic = star1_df.iloc[np.where(m_tgas_epic)[0]]
star2_tgas_epic = star2_df.iloc[np.where(m_tgas_epic)[0]]
print(len(np.where(m_tgas_epic)[0]), "pairs found in K2")

print(len(star1_tgas_epic.source_id))
print(len(np.unique(star1_tgas_epic.source_id.values)))
print(len(star2_tgas_epic.source_id))
print(len(np.unique(star2_tgas_epic.source_id.values)))

star1_kic = pd.merge(star1_tgas, kplr_tgas, on=star1_tgas.columns.tolist(),
                     how='left')
star2_kic = pd.merge(star2_tgas, kplr_tgas, on=star2_tgas.columns.tolist(),
                     how='left')
star1_epic = pd.merge(star1_tgas_epic, epic_tgas,
                      on=star1_tgas.columns.tolist(), how='left')
star2_epic = pd.merge(star2_tgas_epic, epic_tgas,
                      on=star2_tgas.columns.tolist(), how='left')
print(np.shape(star1_kic), np.shape(star2_kic), np.shape(star1_epic),
      np.shape(star2_epic))
assert 0

m1_kplr = kplr_tgas.source_id.isin(star1_tgas.source_id).values
m2_kplr = kplr_tgas.source_id.isin(star2_tgas.source_id).values
star1_kic = kplr_tgas.iloc[np.where(m1_kplr)[0]]
star2_kic = kplr_tgas.iloc[np.where(m2_kplr)[0]]
print(len(np.where(m1_kplr)[0]), "pairs found again in kepler")
print(len(np.where(m2_kplr)[0]), "pairs found again in kepler")
print(np.shape(star1_kic))
print(star1_kic.keys())

plt.clf()
for i, _ in enumerate(star1_kic.ra.values):
    plt.plot([star1_kic.ra.values[i], star2_kic.ra.values[i]],
             [star1_kic.dec.values[i], star2_kic.dec.values[i]])
plt.plot(star1_kic.ra, star1_kic.dec, "r.")
plt.plot(star2_kic.ra, star2_kic.dec, "k.")
plt.savefig("kepler_ra_dec")
assert 0

# do the same for the epic
m_tgas = star1_df.source_id.isin(epic_tgas.source_id).values * \
    star2_df.source_id.isin(epic_tgas.source_id).values
star1_tgas = star1_df.iloc[np.where(m_tgas)]
star2_tgas = star2_df.iloc[np.where(m_tgas)]
m1_epic = kplr_tgas.source_id.isin(star1_tgas.source_id).values
m2_epic = kplr_tgas.source_id.isin(star2_tgas.source_id).values
star1_epic = kplr_tgas.iloc[np.where(m1_epic)]
star2_epic = kplr_tgas.iloc[np.where(m2_epic)]

print(np.shape(star1_epic))

plt.clf()
for i, _ in enumerate(star1_epic.ra.values):
    plt.plot([star1_epic.ra.values[i], star2_epic.ra.values[i]],
             [star1_epic.dec.values[i], star2_epic.dec.values[i]])
plt.plot(star1_epic.ra, star1_epic.dec, "k.")
plt.plot(star2_epic.ra, star2_epic.dec, "k.")
# plt.xlim(230, 270)
# plt.ylim(-30, -12)
plt.savefig("k2_ra_dec")
