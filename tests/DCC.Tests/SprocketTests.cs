using DCC.SprocketLib;

namespace DCC.Tests;

public class SprocketTests
{
    public void Constructor_DefaultValues_AreProperlyInitialized()
    {
        var sprocket = new Sprocket
        {
            Sku = "SPRK-001",
            Name = "Default Test Sprocket"
        };

        Assert.NotEqual(Guid.Empty, sprocket.Id);
        Assert.Equal(HubType.TypeB, sprocket.Hub);
    }

    [Theory]
    [InlineData(12, 12.7, 49.07)]
    [InlineData(40, 12.7, 161.87)]
    [InlineData(20, 25.4, 162.37)]
    public void PitchDiameterMm_CalculatesAccurately(int teeth, double pitch, double expectedDiameter)
    {
        var sprocket = new Sprocket
        {
            Sku = "TEST-SPRK",
            Name = "Calculated Sprocket",
            TeethCount = teeth,
            PitchMm = pitch
        };

        var result = sprocket.PitchDiameterMm;

        Assert.Equal(expectedDiameter, result, precision: 2);

    }
}