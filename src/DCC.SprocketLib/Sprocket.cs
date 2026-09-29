namespace DCC.SprocketLib;

public class Sprocket
{
    public Guid Id { get; init; } = Guid.NewGuid();

    public required string Sku { get; set; }

    public required string Name { get; set; }

    public int TeethCount { get; set; }

    public double PitchMm { get; set; }

    public double BoreDiameterMm { get; set; }

    public HubType Hub { get; set; } = HubType.TypeB;

    public decimal UnitPrice {get; set; }

    public double PitchDiameterMm =>
        TeethCount > 0 ? PitchMm / Math.Sin(Math.PI / TeethCount) : 0;
}