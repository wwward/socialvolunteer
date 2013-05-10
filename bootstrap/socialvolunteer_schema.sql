SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `groupwerk` DEFAULT CHARACTER SET latin1 ;
USE `groupwerk` ;

-- -----------------------------------------------------
-- Table `groupwerk`.`Friends`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Friends` (
  `id` INTEGER,
  `friend_id` INTEGER)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_friends` ON `groupwerk`.`Friends` (`id` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Job`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Job` (
  `id` INTEGER AUTO_INCREMENT,
  `organization_id` INTEGER ,
  `event_date` DATE NULL DEFAULT NULL ,
  `event_time` TIME NULL DEFAULT NULL ,
  `event_duration_minutes` SMALLINT(6) NULL DEFAULT NULL ,
  `score_value` SMALLINT(6) NULL DEFAULT NULL ,
  `title` VARCHAR(100) NULL DEFAULT NULL ,
  `description` TEXT NULL DEFAULT NULL ,
  `location` VARCHAR(100) NULL DEFAULT NULL ,
  `category` VARCHAR(255) NULL DEFAULT NULL ,
  `status` SMALLINT(6) NULL DEFAULT NULL,
  PRIMARY KEY(id)
  ) AUTO_INCREMENT = 10000
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Job_volunteer`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Job_volunteer` (
  `job_id` INTEGER ,
  `volunteer_id` INTEGER ,
  `committed` SMALLINT(6) NULL DEFAULT NULL ,
  `completed` SMALLINT(6) NULL DEFAULT NULL ,
  `checkedin` SMALLINT(6) NULL DEFAULT NULL ,
  `checkedout` SMALLINT(6) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Keyword`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Keyword` (
  `keyword` VARCHAR(30) NULL DEFAULT NULL ,
  `reference_id` INTEGER )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_keyword` ON `groupwerk`.`Keyword` (`keyword` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Organization`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Organization` (
  `id` INTEGER AUTO_INCREMENT ,
  `name` VARCHAR(60) NULL DEFAULT NULL ,
  `phone` VARCHAR(15) NULL DEFAULT NULL ,
  `email` VARCHAR(60) NULL DEFAULT NULL ,
  `location` VARCHAR(60) NULL DEFAULT NULL ,
  `reputation` SMALLINT(6) NULL DEFAULT NULL ,
  `description` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (id)
  ) AUTO_INCREMENT=5000 
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_organization` ON `groupwerk`.`Organization` (`location` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Score`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Score` (
  `id` INTEGER ,
  `job_id` INTEGER ,
  `score` SMALLINT(6) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_score` ON `groupwerk`.`Score` (`id` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Volunteer`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Volunteer` (
  `id` INTEGER AUTO_INCREMENT,
  `name` VARCHAR(60) NULL DEFAULT NULL ,
  `email` VARCHAR(60) NULL DEFAULT NULL ,
  `phone` VARCHAR(15) NULL DEFAULT NULL ,
  `location` VARCHAR(60) NULL DEFAULT NULL ,
  `reputation` SMALLINT(6) NULL DEFAULT NULL ,
  `username` VARCHAR(30) NULL DEFAULT NULL,
  PRIMARY KEY(id)
  ) AUTO_INCREMENT=1000
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_volunteer` ON `groupwerk`.`Volunteer` (`location` ASC) ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
