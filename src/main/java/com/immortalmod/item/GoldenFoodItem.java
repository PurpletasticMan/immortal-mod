package com.immortalmod.item;

import java.util.List;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** Food that also hands out status effects when eaten. */
public class GoldenFoodItem extends Item {
	private final List<MobEffectInstance> effects;

	public GoldenFoodItem(Properties properties, List<MobEffectInstance> effects) {
		super(properties);
		this.effects = effects;
	}

	@Override
	public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
		ItemStack result = super.finishUsingItem(stack, level, entity);
		if (level instanceof ServerLevel) {
			for (MobEffectInstance effect : effects) {
				entity.addEffect(new MobEffectInstance(effect));
			}
		}
		return result;
	}
}
